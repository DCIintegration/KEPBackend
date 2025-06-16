class FinancialInformation:  # Corregir nombre de clase
    
    @staticmethod
    def calcular_nomina_mensual(empleados, departamento=None):
        """
        Calcula la nómina mensual de empleados.
        Si se proporciona un departamento, calcula solo para ese departamento.
        """
        if departamento:
            empleados_filtrados = empleados.filter(departamento=departamento, activo=True)
        else:
            empleados_filtrados = empleados.filter(activo=True)
        
        return sum(empleado.sueldo for empleado in empleados_filtrados)

    @staticmethod
    def empleados_facturables(empleados):
        """
        Retorna la cantidad de empleados que son facturables,
        es decir, aquellos que pertenecen a Diseño o Ingeniería.
        """
        return empleados.filter(
            departamento__nombre__icontains='Diseño',
            activo=True
        ).count() + empleados.filter(
            departamento__nombre__icontains='Ingenieria',
            activo=True
        ).count()

    @staticmethod
    def horas_facturables(empleados):
        """
        Calcula las horas facturables basadas en empleados facturables.
        """
        empleados_fact = FinancialInformation.empleados_facturables(empleados)
        return empleados_fact * 8.5 * 22  # 8.5 horas por día, 22 días laborables

    @staticmethod
    def horas_plantas(empleados):
        """
        Calcula las horas planta de todos los empleados.
        """
        total_empleados = empleados.filter(activo=True).count()
        return total_empleados * 8.5 * 22