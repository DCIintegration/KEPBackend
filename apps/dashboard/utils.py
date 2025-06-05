from dataclasses import dataclass

@dataclass
class KPIData:
    total_horas_facturables: float
    total_horas_facturadas: float
    costo_por_hora: float
    ganancia_total: float
    numero_empleados: int
    numero_empleados_facturables: int
    dias_trabajados: int


class KPI_Calculator:
    @staticmethod
    def EBLR(kpi_data):
        return kpi_data.total_horas_facturables * kpi_data.costo_por_hora  #Pendiente indirect labor revenue 

    @staticmethod
    def RE(kpi_data):
        return kpi_data.ganancia_total / kpi_data.numero_empleados

    @staticmethod
    def RBE(kpi_data):
        return kpi_data.ganancia_total / kpi_data.numero_empleados_facturables #Gnanacia total con estuardo, pendiente de sacar ese calculo de manera automatica

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

    def calculate_KPI(self, kpi_name, kpi_data):
        kpi_methods = {method: getattr(self, method) for method in dir(self) if callable(getattr(self, method)) and not method.startswith("_")}
        
        if kpi_name in kpi_methods:
            return kpi_methods[kpi_name](kpi_data)
        else:
            raise ValueError("KPI no encontrado")