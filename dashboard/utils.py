class KPI:
    """ Clase de Indicadores Clave de Desempeño (KPI) """

    @staticmethod
    def ELDR(horas_facturables, costo):
        return horas_facturables * costo

    @staticmethod
    def RE(ganancias_totales, numero_empleados):
        return ganancias_totales / numero_empleados

    @staticmethod
    def RBE(ganancia_total, numero_empleados_facturables):
        return ganancia_total / numero_empleados_facturables

    @staticmethod
    def UBH(horas_facturadas, numero_empleados_facturables, dias_trabajados):
        total_horas = ((numero_empleados_facturables * 8.5) * numero_empleados_facturables) * dias_trabajados
        return horas_facturadas / total_horas

    @staticmethod
    def UB(total_horas_dobico, dias_trabajados, numero_empleados_facturables):
        total_horas = ((numero_empleados_facturables * 8.5) * numero_empleados_facturables) * dias_trabajados
        return total_horas_dobico / total_horas

    @staticmethod
    def LM(ganancia_total, costo_empleado_hora):
        return ganancia_total / costo_empleado_hora

    @staticmethod
    def LMM(numero_empleados_facturables, dato_admin):
        return 8.5 * numero_empleados_facturables

    @staticmethod
    def DB(backlog_hours, available_hours_per_day):
        return backlog_hours / available_hours_per_day

    @staticmethod
    def DCH(cash_balance, loc_avail, average_daily_spend):
        return (cash_balance + loc_avail) / average_daily_spend