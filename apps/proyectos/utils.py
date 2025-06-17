import os
import django
#import threading
import chardet
import pandas as pd
from django.db.models import Max

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KEP.settings')
django.setup()

from apps.proyectos.models import RegistroHoras

class LoadData():

    def convertir_a_utf8(file):
        """Convierte cualquier archivo a UTF-8 y retorna un objeto StringIO"""
        from io import StringIO
        
        encodings_to_try = ['utf-16', 'utf-16-le', 'cp1252', 'utf-8', 'latin1']
        
        for encoding in encodings_to_try:
            try:
                file.seek(0)
                content = file.read()
                
                # Decodificar con la codificación actual
                if isinstance(content, bytes):
                    decoded_content = content.decode(encoding)
                else:
                    decoded_content = content
                
                # Retornar como StringIO (que es UTF-8 internamente)
                return StringIO(decoded_content)
                
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception:
                continue
        
        raise ValueError("No se pudo convertir el archivo a UTF-8")

    def load_csv(file):
        # Convertir cualquier archivo a UTF-8 primero
        file_utf8 = LoadData.convertir_a_utf8(file)
        
        # Ahora leer con UTF-8 garantizado
        df = pd.read_csv(file_utf8, encoding='utf-8')
        
        print(f"Total de filas en el CSV: {len(df)}")
        
        # DEBUG: Ver qué formato tienen las fechas realmente
        print("Primeras 5 fechas en el archivo:")
        print(df['Date'].head().tolist())
        print(f"Tipo de datos de la columna Date: {df['Date'].dtype}")
        
        ultima_fecha = RegistroHoras.objects.aggregate(Max('date'))['date__max']
        print(f"Última fecha en BD: {ultima_fecha}")
        
        # Intentar múltiples formatos de fecha
        df['Date'] = pd.to_datetime(df["Date"], errors='coerce', infer_datetime_format=True)
        
        # Si sigue fallando, intentar formatos específicos
        if df['Date'].isna().all():
            formatos_fecha = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']
            for formato in formatos_fecha:
                try:
                    df['Date'] = pd.to_datetime(df["Date"], format=formato, errors='coerce')
                    if not df['Date'].isna().all():
                        print(f"Formato de fecha que funcionó: {formato}")
                        break
                except:
                    continue
        
        print(f"Fechas después de conversión (primeras 5):")
        print(df['Date'].head().tolist())
        
        df = df.dropna(subset=['Date'])
        print(f"Filas después de limpiar fechas: {len(df)}")
        
        # Resto del código igual...
        df = df.sort_values(by="Date")
        df[['OT', 'Planta']] = df['Project'].str.extract(r'((?:OT\d{2}-\d{1}-\d{3,5}|DCI-\d{2}))\s*[-–]?\s*(.*)')
        df.drop(columns=['Project'], inplace=True)
        df = df[df['Time Entry Status'] == 'Submitted']
        print(f"Filas después de filtrar 'Submitted': {len(df)}")
        
        if ultima_fecha:
            df = df[df['Date'].dt.date > ultima_fecha]
            print(f"Filas después de filtrar por fecha: {len(df)}")
        
 
        
        registros_creados = 0
        registros_actualizados = 0
        errores = 0
        
        for _, row in df.iterrows():
            try:
                hours_worked = float(row['Hours Worked']) if pd.notna(row['Hours Worked']) else 0.0
                
                obj, created = RegistroHoras.objects.update_or_create(
                    date=row['Date'],
                    employee=row['Employee'],
                    task=row['Task'],
                    defaults={
                        'time_entry_status': row['Time Entry Status'],
                        'hours_worked': hours_worked,
                        'employee_group': row['Employee Group'],
                        'manager': row['Manager'],
                        'project_status': row['Project Status (Count)'] == 'Active',
                        'ot': row['OT'] if pd.notna(row['OT']) else '',
                        'planta': row['Planta'] if pd.notna(row['Planta']) else ''
                    }
                )
                
                if created:
                    registros_creados += 1
                else:
                    registros_actualizados += 1
                    
            except Exception as e:
                print(f"Error al cargar la fila {row.to_dict()}: {e}")
                errores += 1
                continue
        
        print(f"Resumen: {registros_creados} creados, {registros_actualizados} actualizados, {errores} errores")
        
        # Verificar que se guardaron en la BD
        total_registros = RegistroHoras.objects.count()
        print(f"Total de registros en BD después de la carga: {total_registros}")
        
        return {
            'creados': registros_creados,
            'actualizados': registros_actualizados,
            'errores': errores,
            'total_bd': total_registros
        }

        

            #Añadir columna de facturable o no facturable 