class FinantialInformation:

    def calcular_nomina_mensual(Empleado, Departamento):
        """
        Calcula la nómina mensual de un departamento.
        """
        for empleado in Empleado:
            if empleado.departamento == Departamento:   
               Departamento.nomina_mensual += empleado.sueldo
        return Departamento.nomina_mensual   

    def empleados_facturables(Empleado):
        """
        Retorna la cantidad de empleados que son facturables,
        es decir, aquellos que pertenecen a Diseño o Ingeniería.
        """
        count = 0
        for empleado in Empleado:
            if empleado.departamento and empleado.departamento.nombre.lower() in ['diseño', 'ingenieria']:
                count += 1
        return count

    
    def horas_facturables(Empleado):
        """
        Filtra y retorna una lista de horas facturables.
        """
        horas = FinantialInformation.empleados_facturables(Empleado) * 8.5
        return horas

    def horas_plantas(Empleado):
        """
        Filtra y retorna una lista de horas planta.
        """
        pass