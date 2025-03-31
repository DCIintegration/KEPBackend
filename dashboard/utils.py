from django.shortcuts import get_object_or_404
import openai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from dashboard.models import KpiInputData
from datetime import timedelta

class Utils:
    @staticmethod
    def ELDR(kpi_data):
        return kpi_data.total_horas_facturables * kpi_data.costo_por_hora

    @staticmethod
    def RE(kpi_data):
        return kpi_data.ganancia_total / kpi_data.numero_empleados

    @staticmethod
    def RBE(kpi_data):
        return kpi_data.ganancia_total / kpi_data.numero_empleados_facturables

    @staticmethod
    def UBH(kpi_data):
        total_horas = ((kpi_data.numero_empleados_facturables * 8.5) * kpi_data.numero_empleados_facturables) * kpi_data.dias_trabajados
        return kpi_data.total_horas_facturadas / total_horas

    @staticmethod
    def UB(kpi_data):
        total_horas = ((kpi_data.numero_empleados_facturables * 8.5) * kpi_data.numero_empleados_facturables) * kpi_data.dias_trabajados
        return kpi_data.total_horas_facturables / total_horas

    @staticmethod
    def LM(kpi_data):
        return kpi_data.ganancia_total / kpi_data.costo_por_hora

    @staticmethod
    def LMM(kpi_data):
        return 8.5 * kpi_data.numero_empleados_facturables

 

    
    def generate_kpi_explanation(kpi,kpi_input_data_id):
        """
        Generate a detailed explanation of the KPI using OpenAI API
        """
        kpi_input_data = get_object_or_404(KpiInputData, id=kpi_input_data_id)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a business intelligence expert explaining KPIs in a professional, detailed manner."
                    },
                    {
                        "role": "user", 
                        "content": f"""Provide a comprehensive explanation of the {kpi.name} KPI (Code: {kpi.code}).
                        Also I want you to generate a citical analisis for this KPI based on the following data 
                        - Total Billable Hours: {kpi_input_data.total_horas_facturables}
                        - Total Plant Hours: {kpi_input_data.total_horas_planta}
                        - Total Billed Hours: {kpi_input_data.total_horas_facturadas}
                        - Number of Employees: {kpi_input_data.numero_empleados}
                        - Number of Billable Employees: {kpi_input_data.numero_empleados_facturables}
                        - Days Worked: {kpi_input_data.dias_trabajados}
                        - Cost per Hour: {kpi_input_data.costo_por_hora}
                        - Total Profit: {kpi_input_data.ganancia_total}
                        Include the following details:
                        - What does this KPI measure?
                        - Why is it important for businesses?
                        - How is it typically calculated?
                        - What are the best practices for improving this KPI?
                        - What are potential challenges in tracking this KPI?
                        
                        Write in a professional, informative tone, suitable for a business report."""
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating AI explanation: {str(e)}")
            return f"AI-generated explanation unavailable. KPI Description: {kpi_input_data.description}"
    
#Funcion para generar un reporte pdf, haciendo uso de la funcion generate_kpi_explanation
#Queda pendiente la implementacion de la libreria para generar el pdf
    def generate_report():

        report = canvas.Canva("kpi_report.pdf", pagesize= (letter))


        return 


    def filter_data_by_date(data, start_date, end_date):
        """
        Filter data based on a date range.
        """
        filtered_data = {}
        
        current_date = start_date
        while current_date <= end_date:
            if current_date in data:
                filtered_data[current_date] = data[current_date]
            current_date += timedelta(days=1)

        return filtered_data
