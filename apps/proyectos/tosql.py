import os 
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KEP.settings') 
django.setup()
import csv
from .models import RegistroHoras

def cargar_datos_desde_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
         
                registro = RegistroHoras(
                    date=row['Date'],
                    time_entry_status=row['Time Entry Status'],
                    task=row['Task'],
                    hours_worked=float(row['Hours Worked']),  # Asegúrate de que sea un entero
                    employee=row['Employee'],
                    employee_group=row['Employee Group'],
                    manager=row['Manager'],
                    project_status = row['Project Status (Count)'] == 'Active',
                    ot=row['OT'],
                    planta=row['Planta']
                )
                
                # Guardar el objeto en la base de datos
                registro.save()
            
            except Exception as e:
                # Manejo de errores para cada fila
                print(f"Error al cargar la fila {row}: {e}")
                continue

"""
Si se sube un csv de datos que ya existem, se tiene que ignorar siempre y cuando sean iguales, de lo contrario se deben de actualizar los datos
"""

def main():

    file_path = 'apps/proyectos/DemoHoras.csv'  # Cambia esto al path de tu archivo CSV
    cargar_datos_desde_csv(file_path)
    print("Datos cargados exitosamente.")

if __name__ == "__main__":
    main()