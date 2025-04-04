from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import Kpi, KpiTarget
import json


# Vista disponible para todos los usuarios, muestra los KPIs
@login_required(login_url="custom_auth/login/")
def mainDashboard():
    kpis = list(Kpi.objects.values("id", "name", "code", "description", "kpi_type", "unit"))
    return JsonResponse({"KPIs": kpis})

# Vista disponible solo para el superusuario
@login_required(login_url="custom_auth/login/")
def create_KPI(request):
    if request.user.is_superuser:
        if request.method =="POST":
            try:
                data = json.loads(request.body)

                kpi, created = Kpi.objects.get_or_create(
                    defaults={
                        "code": data["code"],
                        "name": data["name"],
                        "description": data["description"],
                        "kpi_type": data["kpi_type"],
                        "unit": data["unit"],
                    }
                )
                if created:
                    return JsonResponse({"message": f"KPI {kpi.nombre} creado exitosamente"})
                else:
                    return JsonResponse("error:" "Este KPI ya existe")
            except:
                return JsonResponse()
    return JsonResponse({"error": "No tienes permisos para crear un KPI"}, status=403)

# Vista disponible para el superusuario y administración
@login_required(login_url="custom_auth/login/")
def update_KPI(request, kpi_id):
    if request.user.is_superuser or request.user.is_admin():
        
        if request.method == "POST":
            try:
                kpi = get_object_or_404(Kpi, id=kpi_id)
                data = json.loads(request.body)

                kpi.code = data.get("code", kpi.code)
                kpi.name = data.get("name", kpi.name)
                kpi.description = data.get("description", kpi.description)
                kpi.kpi_type = data.get("kpi_type", kpi.kpi_type)
                kpi.unit = data.get("unit", kpi.unit)

                kpi.save()
                return JsonResponse({"message": f"KPI {kpi.name} actualizado correctamente"})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
            
    else:
        return JsonResponse({"error": "No tienes permisos para actualizar un KPI"}, status=405)
    

# Vista disponible solo para el superusuario
@login_required(login_url="custom_auth/login/")
def delete_KPI(request, kpi_id):
    if request.user.is_superuser:
        kpi = get_object_or_404(Kpi, id=kpi_id)
        kpi.delete()
        return JsonResponse({"message": f"KPI {kpi.name} eliminado correctamente"})
    return JsonResponse({"error": "No tienes permisos para eliminar un KPI"}, status=403)

# Vista disponible para todos los usuarios, muestra detalles de un KPI
@login_required(login_url="custom_auth/login/")
def view_KPI_details(kpi_id):
    kpi = get_object_or_404(Kpi, id=kpi_id)
    return JsonResponse({
        "id": kpi.id,
        "nombre": kpi.name,
        "code": kpi.code,
        "descripcion": kpi.description,
        "tipo": kpi.kpi_type,
        "unidad": kpi.unit,
    })

@login_required(login_url="custom_auth/login/")
def view_KPI_goal():
    kpi_goals = list(KpiTarget.objects.values("id", "kpi__name", "period", "target_value", "min_value", "max_value"))
    return JsonResponse({"KPI Goals": kpi_goals})

@login_required(login_url="custom_auth/login/")
def edit_KPI_goal(request, kpi_goal_id):
    if request.user.is_superuser or request.user.is_admin():
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                kpi_goal = get_object_or_404(KpiTarget, id=kpi_goal_id)

                kpi_goal.kpi = data.get("kpi", kpi_goal.kpi)
                kpi_goal.period = data.get("period", kpi_goal.period)
                kpi_goal.target_value = data.get("target_value", kpi_goal.target_value)
                kpi_goal.min_value = data.get("min_value", kpi_goal.min_value)
                kpi_goal.max_value = data.get("max_value", kpi_goal.max_value)

                kpi_goal.save()
                return JsonResponse({"message": f"KPI Goal {kpi_goal.id} actualizado correctamente"})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "No tienes permisos para actualizar un KPI Goal"}, status=403)

@login_required(login_url="custom_auth/login/")
def delete_KPI_goal(request, kpi_goal_id):
    if request.user.is_superuser:
        kpi_goal = get_object_or_404(KpiTarget, id=kpi_goal_id)
        kpi_goal.delete()
        return JsonResponse({"message": f"KPI Goal {kpi_goal.id} eliminado correctamente"})
    return JsonResponse({"error": "No tienes permisos para eliminar un KPI Goal"}, status=403)

@login_required(login_url="custom_auth/login/")
def create_KPI_target(request):
    if request.user.is_superuser:
        if request.method == "POST":
            try:
                data = json.loads(request.body)

                kpi_target, created = KpiTarget.objects.get_or_create(
                    defaults={
                        "kpi": data["kpi"],
                        "period": data["period"],
                        "target_value": data["target_value"],
                        "min_value": data["min_value"],
                        "max_value": data["max_value"],
                    }
                )
                if created:
                    return JsonResponse({"message": f"KPI Target {kpi_target.id} creado exitosamente"})
                else:
                    return JsonResponse({"error": "Este KPI Target ya existe"})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "No tienes permisos para crear un KPI Target"}, status=403)

