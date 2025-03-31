import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from custom_auth.models import Departamento, Empleado

@login_required(login_url="custom_auth/login/")
def dashboard_administrativo(request):
    if request.user.is_admin() or request.user.is_custom_superuser() or request.user.is_superuser:
        departamentos = list(Departamento.objects.values("id", "nombre", "nomina_mensual"))
        return JsonResponse({"departamentos": departamentos})
    return JsonResponse({"error": "No tienes permiso para ver esta información"}, status=403)

@login_required(login_url="custom_auth/login/")
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

@login_required(login_url="custom_auth/login/")
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

@login_required(login_url="custom_auth/login/")
def modificar_datos(request, empleado_id):
    if request.user.is_admin() or request.user.is_custom_superuser() or request.user.is_superuser:
       if request.method == "POST":
        try:
            data = json.loads(request.body)
            empleado = get_object_or_404(Empleado, id=empleado_id)

            empleado.nombre = data.get("nombre", empleado.nombre)
            empleado.role = data.get("role", empleado.role)
            empleado.puesto = data.get("puesto", empleado.puesto)
            empleado.fecha_contratacion = data.get("fecha_contratacion", empleado.fecha_contratacion)
            empleado.activo = data.get("activo", empleado.activo)
            empleado.sueldo = data.get("sueldo", empleado.sueldo)
            empleado.facturable = data.get("facturable", empleado.facturable)

            if "departamento" in data:
                empleado.departamento = get_object_or_404(Departamento, id=data["departamento"]) if data["departamento"] else None

            empleado.save()
            return JsonResponse({"message": f"Usuario {empleado.nombre} actualizado correctamente"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)
