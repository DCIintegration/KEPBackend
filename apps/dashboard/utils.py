# apps/dashboard/utils.py
from dataclasses import dataclass
from datetime import datetime, date
from django.db.models import Sum, Q, Count
from decimal import Decimal
from typing import Optional, Dict, Any

@dataclass
class KPIData:
    total_horas_facturables: float
    total_horas_facturadas: float
    total_horas_planta: float
    costo_por_hora: float
    ganancia_total: float
    numero_empleados: int
    numero_empleados_facturables: int
    dias_trabajados: int
    costo_nomina_total: float = 0
    ingresos_directos: float = 0
    ingresos_indirectos: float = 0

class KPIDataCollector:
    """Clase para recopilar datos reales de la base de datos para cálculos de KPI"""
    
    @staticmethod
    def get_empleados_data(fecha_inicio: date, fecha_fin: date):
        """Obtiene información de empleados activos en el período"""
        from apps.custom_auth.models import Empleado
        
        empleados_activos = Empleado.objects.filter(
            activo=True,
            fecha_contratacion__lte=fecha_fin
        )
        
        # Empleados facturables (departamentos de ingeniería/diseño)
        empleados_facturables = empleados_activos.filter(
            Q(departamento__nombre__icontains='Ingenieria') |
            Q(departamento__nombre__icontains='Diseño') 
        )
        
        return {
            'total_empleados': empleados_activos.count(),
            'empleados_facturables': empleados_facturables.count(),
            'nomina_total': empleados_activos.aggregate(
                total=Sum('sueldo')
            )['total'] or 0,
            'nomina_facturables': empleados_facturables.aggregate(
                total=Sum('sueldo')
            )['total'] or 0
        }
    
    @staticmethod
    def get_horas_data(fecha_inicio: date, fecha_fin: date):
        """Obtiene datos de horas trabajadas del RegistroHoras"""
        from apps.proyectos.models import RegistroHoras
        
        registros = RegistroHoras.objects.filter(
            date__gte=fecha_inicio,
            date__lte=fecha_fin,
            time_entry_status='Submitted'
        )
        
        # Horas totales trabajadas
        total_horas = registros.aggregate(
            total=Sum('hours_worked')
        )['total'] or 0
        
        # Horas facturables (proyectos con OT activos)
        horas_facturables = registros.filter(
            project_status=True,
            ot__isnull=False
        ).exclude(ot='').aggregate(
            total=Sum('hours_worked')
        )['total'] or 0
        
        # Horas por empleado facturable
        from apps.custom_auth.models import Empleado
        empleados_facturables_nombres = Empleado.objects.filter(
            Q(departamento__nombre__icontains='Ingenieria') |
            Q(departamento__nombre__icontains='Diseño'),
            activo=True
        ).values_list('nombre_completo', flat=True)
        
        horas_empleados_facturables = registros.filter(
            employee__in=empleados_facturables_nombres
        ).aggregate(
            total=Sum('hours_worked')
        )['total'] or 0
        
        return {
            'total_horas_planta': float(total_horas),
            'total_horas_facturables': float(horas_empleados_facturables),
            'total_horas_facturadas': float(horas_facturables),
            'dias_unicos_trabajados': registros.values('date').distinct().count()
        }
    
    @staticmethod
    def get_ingresos_data(fecha_inicio: date, fecha_fin: date):
        """Obtiene datos de ingresos de IngresoActividad"""
        from apps.administracion.models import IngresoActividad
        
        # Mapear fechas a mes/año
        meses_periodo = []
        fecha_actual = fecha_inicio.replace(day=1)
        while fecha_actual <= fecha_fin:
            mes_nombre = [
                'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
            ][fecha_actual.month - 1]
            meses_periodo.append((mes_nombre, fecha_actual.year))
            
            # Siguiente mes
            if fecha_actual.month == 12:
                fecha_actual = fecha_actual.replace(year=fecha_actual.year + 1, month=1)
            else:
                fecha_actual = fecha_actual.replace(month=fecha_actual.month + 1)
        
        ingresos_directos = 0
        ingresos_indirectos = 0
        
        for mes, año in meses_periodo:
            ingresos_mes = IngresoActividad.objects.filter(
                month=mes,
                year=año
            ).aggregate(
                directos=Sum('monto', filter=Q(tipo_ingreso='Directo')),
                indirectos=Sum('monto', filter=Q(tipo_ingreso='Indirecto'))
            )
            
            ingresos_directos += ingresos_mes['directos'] or 0
            ingresos_indirectos += ingresos_mes['indirectos'] or 0
        
        return {
            'ingresos_directos': float(ingresos_directos),
            'ingresos_indirectos': float(ingresos_indirectos),
            'ganancia_total': float(ingresos_directos + ingresos_indirectos)
        }
    
    @classmethod
    def collect_kpi_data(cls, fecha_inicio: date, fecha_fin: date, 
                        costo_hora_promedio: float = 250.0) -> KPIData:
        """Método principal para recopilar todos los datos necesarios para KPIs"""
        
        empleados_data = cls.get_empleados_data(fecha_inicio, fecha_fin)
        horas_data = cls.get_horas_data(fecha_inicio, fecha_fin)
        ingresos_data = cls.get_ingresos_data(fecha_inicio, fecha_fin)
        
        # Calcular costo por hora basado en nómina si hay empleados facturables
        if empleados_data['empleados_facturables'] > 0 and horas_data['total_horas_facturables'] > 0:
            costo_calculado = (empleados_data['nomina_facturables'] / 
                             horas_data['total_horas_facturables'])
        else:
            costo_calculado = costo_hora_promedio
        
        return KPIData(
            total_horas_facturables=horas_data['total_horas_facturables'],
            total_horas_facturadas=horas_data['total_horas_facturadas'],
            total_horas_planta=horas_data['total_horas_planta'],
            costo_por_hora=costo_calculado,
            ganancia_total=ingresos_data['ganancia_total'],
            numero_empleados=empleados_data['total_empleados'],
            numero_empleados_facturables=empleados_data['empleados_facturables'],
            dias_trabajados=horas_data['dias_unicos_trabajados'],
            costo_nomina_total=empleados_data['nomina_total'],
            ingresos_directos=ingresos_data['ingresos_directos'],
            ingresos_indirectos=ingresos_data['ingresos_indirectos']
        )

class KPI_Calculator:
    """Calculadora mejorada de KPIs con fórmulas corregidas"""
    
    @staticmethod
    def ELDR(kpi_data: KPIData) -> float:
        """Earnings per Labor Dollar Rate"""
        if kpi_data.costo_nomina_total == 0:
            return 0
        return kpi_data.ganancia_total / kpi_data.costo_nomina_total
    
    @staticmethod
    def RE(kpi_data: KPIData) -> float:
        """Revenue per Employee"""
        if kpi_data.numero_empleados == 0:
            return 0
        return kpi_data.ganancia_total / kpi_data.numero_empleados
    
    @staticmethod
    def RBE(kpi_data: KPIData) -> float:
        """Revenue per Billable Employee"""
        if kpi_data.numero_empleados_facturables == 0:
            return 0
        return kpi_data.ganancia_total / kpi_data.numero_empleados_facturables
    
    @staticmethod
    def UBH(kpi_data: KPIData) -> float:
        """Utilization Billable Hours - % de horas facturadas vs horas facturables"""
        if kpi_data.total_horas_facturables == 0:
            return 0
        return (kpi_data.total_horas_facturadas / kpi_data.total_horas_facturables) * 100
    
    @staticmethod
    def UB(kpi_data: KPIData) -> float:
        """Utilization Benchmark - % de horas facturables vs horas totales de planta"""
        if kpi_data.total_horas_planta == 0:
            return 0
        return (kpi_data.total_horas_facturables / kpi_data.total_horas_planta) * 100
    
    @staticmethod
    def LM(kpi_data: KPIData) -> float:
        """Labor Multiplier"""
        costo_total_labor = kpi_data.total_horas_facturadas * kpi_data.costo_por_hora
        if costo_total_labor == 0:
            return 0
        return kpi_data.ganancia_total / costo_total_labor
    
    @staticmethod
    def LMM(kpi_data: KPIData) -> float:
        """Labor Maximum Multiplier - Horas máximas facturables por empleado"""
        if kpi_data.numero_empleados_facturables == 0:
            return 0
        # Asumiendo 8.5 horas por día por empleado facturable
        return 8.5 * kpi_data.numero_empleados_facturables * kpi_data.dias_trabajados
    
    def calculate_KPI(self, kpi_name: str, kpi_data: KPIData) -> Dict[str, Any]:
        """Calcula un KPI específico y retorna información detallada"""
        kpi_methods = {
            'ELDR': self.ELDR,
            'RE': self.RE,
            'RBE': self.RBE,
            'UBH': self.UBH,
            'UB': self.UB,
            'LM': self.LM,
            'LMM': self.LMM
        }
        
        if kpi_name.upper() not in kpi_methods:
            raise ValueError(f"KPI '{kpi_name}' no encontrado. KPIs disponibles: {list(kpi_methods.keys())}")
        
        valor = kpi_methods[kpi_name.upper()](kpi_data)
        
        return {
            'kpi': kpi_name.upper(),
            'valor': round(valor, 2),
            'datos_utilizados': {
                'periodo_analizado': f"{kpi_data.dias_trabajados} días",
                'empleados_total': kpi_data.numero_empleados,
                'empleados_facturables': kpi_data.numero_empleados_facturables,
                'horas_planta': kpi_data.total_horas_planta,
                'horas_facturables': kpi_data.total_horas_facturables,
                'horas_facturadas': kpi_data.total_horas_facturadas,
                'ganancia_total': kpi_data.ganancia_total,
                'costo_por_hora': kpi_data.costo_por_hora
            }
        }
    
    def calculate_all_KPIs(self, kpi_data: KPIData) -> Dict[str, Any]:
        """Calcula todos los KPIs disponibles"""
        kpis = ['ELDR', 'RE', 'RBE', 'UBH', 'UB', 'LM', 'LMM']
        resultados = {}
        
        for kpi in kpis:
            try:
                resultados[kpi] = self.calculate_KPI(kpi, kpi_data)
            except Exception as e:
                resultados[kpi] = {
                    'kpi': kpi,
                    'error': str(e),
                    'valor': 0
                }
        
        return resultados