import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import webbrowser
from pathlib import Path

class KPIAnalyzer:
    """
    Clase para cálculo y visualización de KPIs con Plotly
    """
    
    @staticmethod
    def calculate_eldr(revenue_directo, revenue_indirecto):
        """Employee Based Labor Revenue"""
        return revenue_directo + revenue_indirecto
    
    @staticmethod
    def calculate_re(ganancias_totales, numero_empleados):
        """Revenue per Employee"""
        return ganancias_totales / numero_empleados
    
    @staticmethod
    def calculate_rbe(ganancia_total, numero_empleados_facturables):
        """Revenue per Billable Employee"""
        return ganancia_total / numero_empleados_facturables
    
    @staticmethod
    def calculate_ubh(horas_facturadas, numero_empleados_facturables, dias_trabajados):
        """Utilization by Hours"""
        total_horas = ((numero_empleados_facturables * 8.5) * dias_trabajados)
        return (horas_facturadas / total_horas) * 100  # Convertir a porcentaje
    
    @staticmethod
    def calculate_ub(total_horas_dobico, dias_trabajados, numero_empleados_facturables):
        """Utilization by Dollars"""
        total_horas = ((numero_empleados_facturables * 8.5) * dias_trabajados)
        return (total_horas_dobico / total_horas) * 100  # Convertir a porcentaje
    
    @staticmethod
    def calculate_lm(ganancia_total, costo_empleado_hora):
        """Labor Multiplier"""
        return ganancia_total / costo_empleado_hora
    
    @staticmethod
    def calculate_lmm(numero_empleados_facturables, dato_admin):
        """Labor Material Mix"""
        return 8.5 * numero_empleados_facturables * dato_admin
    
    @staticmethod
    def calculate_db(backlog_hours, available_hours_per_day):
        """Days in Backlog"""
        return backlog_hours / available_hours_per_day
    
    @staticmethod
    def calculate_dch(cash_balance, loc_avail, average_daily_spend):
        """Days Cash on hand"""
        return (cash_balance + loc_avail) / average_daily_spend

    @staticmethod
    def plot_kpi_trend(df, kpi_name, target_value=None):
        """Gráfico de tendencia para un KPI"""
        fig = px.line(df, x='periodo', y='valor', 
                     title=f'Tendencia {kpi_name}',
                     labels={'valor': kpi_name, 'periodo': 'Periodo'},
                     markers=True)
        
        if target_value is not None:
            fig.add_hline(y=target_value, line_dash="dot",
                         line_color="red", annotation_text="Objetivo")
        
        fig.update_layout(hovermode="x unified")
        return fig
    
    @staticmethod
    def plot_kpi_gauge(current_value, target_value, kpi_name, min_range=0, max_range=100):
        """Gráfico de medidor (gauge)"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_value,
            title={'text': kpi_name},
            gauge={
                'axis': {'range': [min_range, max_range]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, target_value*0.7], 'color': "red"},
                    {'range': [target_value*0.7, target_value*0.9], 'color': "orange"},
                    {'range': [target_value*0.9, target_value*1.1], 'color': "green"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': target_value}}))
        
        fig.update_layout(margin=dict(t=50, b=10))
        return fig

    @classmethod
    def calculate_all_kpis(cls, data_dict):
        """Calcula todos los KPIs"""
        return {
            'ELDR': cls.calculate_eldr(data_dict['revenue_directo'], data_dict['revenue_indirecto']),
            'RE': cls.calculate_re(data_dict['ganancias_totales'], data_dict['numero_empleados']),
            'RBE': cls.calculate_rbe(data_dict['ganancia_total'], data_dict['numero_empleados_facturables']),
            'UBH': cls.calculate_ubh(data_dict['horas_facturadas'], data_dict['numero_empleados_facturables'], data_dict['dias_trabajados']),
            'UB': cls.calculate_ub(data_dict['total_horas_dobico'], data_dict['dias_trabajados'], data_dict['numero_empleados_facturables']),
            'LM': cls.calculate_lm(data_dict['ganancia_total'], data_dict['costo_empleado_hora']),
            'LMM': cls.calculate_lmm(data_dict['numero_empleados_facturables'], data_dict['dato_admin']),
            'DB': cls.calculate_db(data_dict['backlog_hours'], data_dict['available_hours_per_day']),
            'DCH': cls.calculate_dch(data_dict['cash_balance'], data_dict['loc_avail'], data_dict['average_daily_spend'])
        }

def generar_datos_muestra():
    """Genera datos de muestra para 6 meses"""
    datos_base = {
        'revenue_directo': 50000,
        'revenue_indirecto': 20000,
        'ganancias_totales': 70000,
        'numero_empleados': 15,
        'ganancia_total': 70000,
        'numero_empleados_facturables': 10,
        'horas_facturadas': 1200,
        'dias_trabajados': 22,
        'total_horas_dobico': 1100,
        'costo_empleado_hora': 25,
        'dato_admin': 1.2,
        'backlog_hours': 500,
        'available_hours_per_day': 80,
        'cash_balance': 150000,
        'loc_avail': 50000,
        'average_daily_spend': 5000
    }
    
    historical_data = {}
    for i in range(6):
        mes = f'2023-{i+1:02d}'
        # Variación aleatoria de ±20% en los datos
        datos_mes = {k: v * (0.8 + 0.4*(i/5)) for k, v in datos_base.items()}
        historical_data[mes] = datos_mes
    
    return historical_data

def main():
    # Generar datos de muestra
    historical_data = generar_datos_muestra()
    
    # Calcular KPIs para cada mes
    kpis_data = []
    for periodo, datos in historical_data.items():
        kpis = KPIAnalyzer.calculate_all_kpis(datos)
        for kpi, valor in kpis.items():
            kpis_data.append({
                'periodo': periodo,
                'kpi': kpi,
                'valor': valor
            })
    
    df_kpis = pd.DataFrame(kpis_data)
    
    # Crear directorio para guardar gráficos
    output_dir = Path("kpi_output")
    output_dir.mkdir(exist_ok=True)
    
    print("\n=== KPIs del último mes ===")
    ultimo_mes = df_kpis['periodo'].max()
    kpis_ultimo_mes = df_kpis[df_kpis['periodo'] == ultimo_mes]
    
    for _, row in kpis_ultimo_mes.iterrows():
        print(f"{row['kpi']}: {row['valor']:.2f}")
    
    # Generar y guardar gráficos
    print("\nGenerando gráficos...")
    
    # Gráfico de tendencia para RE
    fig_re = KPIAnalyzer.plot_kpi_trend(
        df_kpis[df_kpis['kpi'] == 'RE'],
        'Revenue per Employee',
        target_value=5000
    )
    fig_re.write_html(output_dir / "revenue_per_employee.html")
    
    # Gráfico de medidor para UBH
    ubh_actual = kpis_ultimo_mes[kpis_ultimo_mes['kpi'] == 'UBH']['valor'].values[0]
    fig_ubh = KPIAnalyzer.plot_kpi_gauge(
        current_value=ubh_actual,
        target_value=75,
        kpi_name='Utilization by Hours',
        max_range=100
    )
    fig_ubh.write_html(output_dir / "utilization_hours.html")
    
    # Abrir gráficos en el navegador
    webbrowser.open(str(output_dir / "revenue_per_employee.html"))
    webbrowser.open(str(output_dir / "utilization_hours.html"))
    
    print(f"\nGráficos guardados en: {output_dir.absolute()}")

if __name__ == "__main__":
    main()