from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from custom_auth.models import Departamento, Empleado

@login_required(login_url="/login/")
def dashboard_administrativo(request):
    if request.user.is_admin() or request.user.is_custom_superuser() or request.user.is_superuser:
        departamentos = list(Departamento.objects.values("id", "nombre", "nomina_mensual"))
        return JsonResponse({"departamentos": departamentos})
    return JsonResponse({"error": "No tienes permiso para ver esta información"}, status=403)

@login_required(login_url="/login/")
def departamento_detalles(request, departamento_id):
    if request.user.is_admin() or request.user.is_custom_superuser() or request.user.is_superuser:
        departamento = get_object_or_404(Departamento, id=departamento_id)
        empleados = list(departamento.empleados_departamento().values("id", "nombre", "puesto", "sueldo"))
        return JsonResponse({
            "id": departamento.id,
            "nombre": departamento.nombre,
            "nomina_mensual": departamento.nomina_mensual,
            "empleados": empleados
        })
    return JsonResponse({"error": "No tienes permiso para ver esta información"}, status=403)

@login_required(login_url="/login/")
def empleado_detalles(request, empleado_id):
    if request.user.is_admin() or request.user.is_custom_superuser() or request.user.is_superuser:
        empleado = get_object_or_404(Empleado, id=empleado_id)
        return JsonResponse({
            "id": empleado.id,
            "nombre": empleado.nombre,
            "rol": empleado.role,
            "puesto": empleado.puesto,
            "fecha_contratacion": empleado.fecha_contratacion,
            "activo": empleado.activo,
            "sueldo": empleado.sueldo,
            "departamento": empleado.departamento.nombre if empleado.departamento else None,
            "email": empleado.email,
            "imagen_perfil": empleado.profile_picture.url if empleado.profile_picture else None,
            "facturable": empleado.facturable
        })
    return JsonResponse({"error": "No tienes permiso para ver esta información"}, status=403)

@login_required(login_url="/login/")
def modificar_datos(request, empleado_id):
    if request.user.is_admin() or request.user.is_custom_superuser() or request.user.is_superuser:
        empleado = get_object_or_404(Empleado, id=empleado_id)
        return JsonResponse({
            "id": empleado.id,
            "nombre": empleado.nombre,
            "puesto": empleado.puesto,
            "sueldo": empleado.sueldo
        })
    return JsonResponse({"error": "No tienes permiso para modificar esta información"}, status=403)
