import os
import django
#import threading
import pandas as pd
from django.db.models import Max

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KEP.settings')
django.setup()

from apps.proyectos.models import RegistroHoras

class LoadData():

    def load_csv(file):
        ultima_fecha = RegistroHoras.objects.aggregate(Max('date'))['date__max']
        df = pd.read_csv(file, encoding='utf-16')
        df['Date'] = pd.to_datetime(df["Date"], format='%Y-%m-%d')
        df = df.sort_values(by="Date")
        df[['OT', 'Planta']] = df['Project'].str.extract(r'((?:OT\d{2}-\d{1}-\d{3,5}|DCI-\d{2}))\s*[-–]?\s*(.*)')
        df.drop(columns=['Project'], inplace=True)
        df = df[df['Time Entry Status']== 'Submitted']

        # Convertir la columna Date a solo fecha (sin hora)
        if ultima_fecha:
            df = df[df['Date'].dt.date > ultima_fecha]

        for _, row in df.iterrows():
            try:
                obj, created = RegistroHoras.objects.update_or_create(
                    date=row['Date'],
                    employee=row['Employee'],
                    task=row['Task'],
                    defaults={
                        'time_entry_status': row['Time Entry Status'],
                        'hours_worked': float(row['Hours Worked']),
                        'employee_group': row['Employee Group'],
                        'manager': row['Manager'],
                        'project_status': row['Project Status (Count)'] == 'Active',
                        'ot': row['OT'],
                        'planta': row['Planta']
                    }
                )
            except Exception as e:
                print(f"Error al cargar la fila {row.to_dict()}: {e}")
                continue
