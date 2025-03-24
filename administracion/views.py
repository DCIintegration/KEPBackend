from django.shortcuts import get_object_or_404, render
from custom_auth.models import Departamento, Empleado

# Dashboard que muestra los departamentos activos dentro de la empresa
def dashboard_administrativo(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if not empleado.is_authenticated:
        return render(request, "../templates/login.html")

    if empleado.is_admin() or empleado.is_superusuario():
        departamentos = Departamento.objects.all()
        return render(request, "../templates/dashboard.html", {"Departamentos": departamentos})

    return render(request, "../templates/sin_permiso.html", {"Nombre": empleado.nombre})


# Detalles del departamento (si aplica mostrará los empleados de cada departamento)
def departamento_detalles(request, departamento_id, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if not empleado.is_authenticated:
        return render(request, "../templates/login.html")

    if empleado.is_admin() or empleado.is_superusuario():
        departamento = get_object_or_404(Departamento, id=departamento_id)
        return render(request, "../templates/departamento_details.html", {
            "Nombre": departamento.nombre,
            "Nomina_Mensual": departamento.nomina_mensual,
            "Empleados": departamento.empleados_departamento()
        })

    return render(request, "../templates/sin_permiso.html", {"Nombre": empleado.nombre})


# Detalles de cada empleado
def empleado_detalles(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if not empleado.is_authenticated:
        return render(request, "../templates/login.html")

    if empleado.is_admin() or empleado.is_superusuario():
        return render(request, "../templates/detalles_empleado.html", {
            "Nombre": empleado.nombre,
            "Rol": empleado.role,
            "Puesto": empleado.puesto,
            "Fecha_Contratacion": empleado.fecha_contratacion,
            "Activo": empleado.activo,
            "Sueldo": empleado.sueldo,
            "Departamento": empleado.departamento,
            "Email": empleado.email,
            "Imagen_Perfil": empleado.profile_picture,
            "Facturable": empleado.facturable
        })

    return render(request, "../templates/sin_permiso.html", {"Nombre": empleado.nombre})


# Editar datos administrativos de empleados
def modificar_datos(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if not empleado.is_authenticated:
        return render(request, "../templates/login.html")

    if empleado.is_admin() or empleado.is_superusuario():
        return render(request, "../templates/modificar_datos.html", {"Empleado": empleado})

    return render(request, "../templates/sin_permiso.html", {"Nombre": empleado.nombre})
