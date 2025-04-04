# apps/utils/file_processors.py
import pandas as pd
from collections import defaultdict
from django.core.files.storage import default_storage
import os
import logging

logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self, log_function=None, is_plant_task_function=None):
        self.log = log_function if log_function else logger.info
        self.error_log = logger.error
        
        # Función para determinar si una actividad es de planta
        self.is_plant_task = is_plant_task_function if is_plant_task_function else self._default_is_plant_task
    
    def _default_is_plant_task(self, actividad):
        """Implementación predeterminada para identificar tareas de planta"""
        keywords = ['planta', 'mantenimiento', 'operación', 'maquinaria']
        return any(keyword.lower() in actividad.lower() for keyword in keywords)
    
    def process_file(self, file_path, file_type="total"):
        """Procesa un archivo Excel o CSV y devuelve los datos procesados"""
        self.log(f"Procesando archivo {file_path} como {file_type}")
        
        # Diccionarios para almacenar la información procesada
        horas_por_ot = defaultdict(lambda: {"total": 0, "planta": 0})
        horas_mensuales_por_ot = defaultdict(lambda: {"total": 0, "planta": 0})
        info_por_ot = {}
        empleados_set = set()  # Para contar empleados únicos
        
        # Determinar el tipo de archivo por su extensión
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension in ['.xlsx', '.xls']:
                self._process_excel(file_path, file_type, horas_por_ot, horas_mensuales_por_ot, info_por_ot, empleados_set)
            elif file_extension == '.csv':
                self.process_raw_data(file_path, file_type, horas_por_ot, horas_mensuales_por_ot, info_por_ot, empleados_set)
            else:
                self.error_log(f"Tipo de archivo no soportado: {file_extension}")
                return None
                
            # Calcular resumen de datos para KPIs
            total_horas_facturables = sum(ot_data["total"] for ot_data in horas_por_ot.values())
            total_horas_planta = sum(ot_data["planta"] for ot_data in horas_por_ot.values())
            numero_empleados = len(empleados_set)
                
            return {
                "horas_por_ot": dict(horas_por_ot),
                "horas_mensuales_por_ot": dict(horas_mensuales_por_ot),
                "info_por_ot": info_por_ot,
                "resumen": {
                    "total_horas_facturables": total_horas_facturables,
                    "total_horas_planta": total_horas_planta,
                    "numero_empleados": numero_empleados
                }
            }
            
        except Exception as e:
            self.error_log(f"Error procesando archivo {file_path}: {str(e)}")
            return None
    
    def _process_excel(self, file_path, file_type, horas_por_ot, horas_mensuales_por_ot, info_por_ot, empleados_set):
        """Procesa archivos Excel"""
        try:
            df = pd.read_excel(file_path)
            
            # Verificar que el DataFrame tenga las columnas necesarias
            required_columns = ['OT', 'Cliente', 'Empleado', 'Actividad', 'Horas']
            
            # Intentar mapear columnas si no coinciden exactamente
            column_mapping = {}
            for col in df.columns:
                for req_col in required_columns:
                    if req_col.lower() in col.lower():
                        column_mapping[req_col] = col
                        break
            
            # Si no se encontraron todas las columnas requeridas, usar las primeras 5 columnas
            if len(column_mapping) < len(required_columns):
                self.log("No se encontraron todas las columnas requeridas, usando las primeras 5 columnas")
                if len(df.columns) >= 5:
                    column_mapping = {
                        'OT': df.columns[0],
                        'Cliente': df.columns[1],
                        'Empleado': df.columns[2],
                        'Actividad': df.columns[3],
                        'Horas': df.columns[4]
                    }
                else:
                    raise ValueError("El archivo no tiene suficientes columnas")
            
            # Procesar cada fila del DataFrame
            for _, row in df.iterrows():
                try:
                    ot = str(row[column_mapping['OT']]) if pd.notna(row[column_mapping['OT']]) else ""
                    cliente = str(row[column_mapping['Cliente']]) if pd.notna(row[column_mapping['Cliente']]) else ""
                    empleado = str(row[column_mapping['Empleado']]) if pd.notna(row[column_mapping['Empleado']]) else ""
                    actividad = str(row[column_mapping['Actividad']]) if pd.notna(row[column_mapping['Actividad']]) else ""
                    
                    # Añadir empleado al conjunto de empleados únicos
                    if empleado:
                        empleados_set.add(empleado)
                    
                    # Convertir horas a float
                    horas_val = row[column_mapping['Horas']]
                    horas = float(horas_val) if pd.notna(horas_val) else 0
                    
                    # Almacenar información por OT
                    if file_type == "total":
                        horas_por_ot[ot]["total"] += horas
                        if self.is_plant_task(actividad):
                            horas_por_ot[ot]["planta"] += horas
                    elif file_type == "mensual":
                        horas_mensuales_por_ot[ot]["total"] += horas
                        if self.is_plant_task(actividad):
                            horas_mensuales_por_ot[ot]["planta"] += horas
                    
                    info_por_ot[ot] = {"cliente": cliente}
                except Exception as e:
                    self.error_log(f"Error procesando fila: {str(e)}")
                    continue
                
            self.log(f"Procesamiento de Excel completado para {file_path}")
            
        except Exception as e:
            self.error_log(f"Error procesando archivo Excel {file_path}: {str(e)}")
            raise
    
    def process_raw_data(self, file_path, file_type, horas_por_ot, horas_mensuales_por_ot, info_por_ot, empleados_set=None):
        """Procesa los datos crudos directamente del archivo CSV"""
        self.log(f"Procesando archivo {file_path} como {file_type}")

        if empleados_set is None:
            empleados_set = set()

        try:
            # Intentar diferentes codificaciones
            encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding, on_bad_lines='skip', 
                                    delimiter=",", quotechar='"')
                    self.log(f"Archivo leído correctamente con codificación {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    self.log(f"Error con codificación {encoding}: {str(e)}")
                    continue
            
            if df is None:
                # Intento final: leer como texto y dividir manualmente
                with open(file_path, 'rb') as f:
                    content = f.read()
                    # Detectar BOM e intentar determinar codificación
                    if content.startswith(b'\xff\xfe'):
                        encoding = 'utf-16-le'
                    elif content.startswith(b'\xfe\xff'):
                        encoding = 'utf-16-be'
                    else:
                        encoding = 'utf-8'
                    
                with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                    lines = f.readlines()
                    # Procesar líneas manualmente
                    for line in lines[1:]:  # Saltar encabezado
                        parts = line.strip().split(',')
                        if len(parts) >= 5:
                            ot = parts[0].strip('"')
                            cliente = parts[1].strip('"')
                            empleado = parts[2].strip('"')
                            actividad = parts[3].strip('"')
                            horas = float(parts[4].strip('"')) if parts[4].strip('"') else 0
                            
                            # Añadir empleado al conjunto
                            if empleado:
                                empleados_set.add(empleado)
                                
                            # Almacenar información por OT
                            if file_type == "total":
                                horas_por_ot[ot]["total"] += horas
                                if self.is_plant_task(actividad):
                                    horas_por_ot[ot]["planta"] += horas
                            elif file_type == "mensual":
                                horas_mensuales_por_ot[ot]["total"] += horas
                                if self.is_plant_task(actividad):
                                    horas_mensuales_por_ot[ot]["planta"] += horas
                            
                            info_por_ot[ot] = {"cliente": cliente}
                    
                    self.log(f"Procesado manual completado para {file_path}")
                    return
            
            # Procesar cada fila del DataFrame
            for _, row in df.iterrows():
                # Obtener datos necesarios (ajustar índices según sea necesario)
                try:
                    if len(df.columns) >= 5:
                        ot = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                        cliente = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                        empleado = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""
                        actividad = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""
                        horas = float(row.iloc[4]) if pd.notna(row.iloc[4]) else 0
                        
                        # Añadir empleado al conjunto
                        if empleado:
                            empleados_set.add(empleado)
                            
                        # Almacenar información por OT
                        if file_type == "total":
                            horas_por_ot[ot]["total"] += horas
                            if self.is_plant_task(actividad):
                                horas_por_ot[ot]["planta"] += horas
                        elif file_type == "mensual":
                            horas_mensuales_por_ot[ot]["total"] += horas
                            if self.is_plant_task(actividad):
                                horas_mensuales_por_ot[ot]["planta"] += horas
                        
                        info_por_ot[ot] = {"cliente": cliente}
                except Exception as e:
                    self.error_log(f"Error procesando fila: {str(e)}")
                    continue
            
            self.log(f"Procesamiento completado para {file_path}")
            
        except Exception as e:
            self.error_log(f"Error procesando archivo {file_path}: {str(e)}")
            raise

    def convertir_csv(self, input_file, output_file):
        """Corrige un CSV manteniendo la estructura, eliminando comillas internas y asegurando que cada campo esté bien delimitado."""
        try:
            # Leer el archivo línea por línea sin procesarlo como DataFrame
            with open(input_file, "r", encoding="utf16") as f:
                lines = f.readlines()

            cleaned_lines = []

            for line in lines:
                # Eliminar comillas internas, pero mantener el delimitador correcto
                import re
                cleaned_line = re.sub(r'(?<!^)"(?!$)', '', line.strip())  # Elimina comillas internas que no están al inicio o final
                
                # Asegurar que toda la línea esté entre comillas
                cleaned_line = f'"{cleaned_line}"'
                
                cleaned_lines.append(cleaned_line)

            # Escribir el archivo corregido
            with open(output_file, "w", encoding="utf16") as f:
                f.writelines("\n".join(cleaned_lines) + "\n")

            self.log(f"Archivo CSV corregido y guardado en {output_file}")

        except Exception as e:
            self.error_log(f"Error al corregir el archivo CSV: {e}")
            raise

    def eliminar_bom(self, file_path):
        """Elimina el BOM (Byte Order Mark) de un archivo UTF-16 si está presente"""
        with open(file_path, 'rb') as f:
            content = f.read()

        # Verificar si el archivo tiene un BOM UTF-16 (código BOM UTF-16 es b'\xff\xfe' o b'\xfe\xff')
        if content.startswith(b'\xff\xfe'):
            content = content[2:]  # Eliminar BOM UTF-16 Little Endian
        elif content.startswith(b'\xfe\xff'):
            content = content[2:]  # Eliminar BOM UTF-16 Big Endian

        # Guardar el archivo sin BOM
        with open(file_path, 'wb') as f:
            f.write(content)
        self.log(f"BOM eliminado de: {file_path}")