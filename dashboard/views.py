from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from custom_auth.models import Empleado
from dashboard.models import Kpi

# Vista disponible para todos los usuarios, muestra los KPIs
@login_required(login_url="/login/")
def dashboard():
    kpis = list(Kpi.objects.values("id", "name", "code", "description", "kpi_type", "unit"))
    return JsonResponse({"KPIs": kpis})

# Vista disponible solo para el superusuario
@login_required(login_url="/login/")
def create_KPI(request):
    if request.user.is_superuser:
        # Aquí puedes agregar la lógica para crear un KPI
        return JsonResponse({"message": "KPI creado exitosamente"})
    return JsonResponse({"error": "No tienes permisos para crear un KPI"}, status=403)

# Vista disponible para el superusuario y administración
@login_required(login_url="/login/")
def update_KPI(request, kpi_id):
    if request.user.is_superuser or request.user.is_admin():
        kpi = get_object_or_404(Kpi, id=kpi_id)
        # Aquí puedes agregar la lógica para actualizar un KPI
        return JsonResponse({"message": f"KPI {kpi.name} actualizado correctamente"})
    return JsonResponse({"error": "No tienes permisos para actualizar un KPI"}, status=403)

# Vista disponible solo para el superusuario
@login_required(login_url="/login/")
def delete_KPI(request, kpi_id):
    if request.user.is_superuser:
        kpi = get_object_or_404(Kpi, id=kpi_id)
        kpi.delete()
        return JsonResponse({"message": f"KPI {kpi.name} eliminado correctamente"})
    return JsonResponse({"error": "No tienes permisos para eliminar un KPI"}, status=403)

# Vista disponible para todos los usuarios, muestra detalles de un KPI
@login_required(login_url="/login/")
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
