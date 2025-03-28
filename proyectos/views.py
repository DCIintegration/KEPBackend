import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
import pandas as pd

from dashboard.models import KpiInputData

from .models import CompanyKPI
from .serializers import CompanyKPISerializer



#quiero ver la info pro la tengo que filtrar con una funcion, asi de sencillo we, tiene que haber una pantalla principal 
#que sea un registro con los diferentes logs de informacion, cada vez que se alimena con info de kpi con filtros

@login_required(login_url="/login/")
def view_logs(request):
    if request.user.is_superuser or request.user.is_proyectos():
        info = list(KpiInputData.objects.values("created_at", "total_horas_facturables", "total_horas_planta", "total_horas_planta", "numero_empleados", "numero_empleados_facturables", "dias_trabajados", "costo_por_hora", "ganancia_total"))
        return JsonResponse(info)
        
    return JsonResponse({"error": "No tienes permiso para ver esta pagina"})

@login_required(login_url="/login/")
def view_log_details(request, KpiInputData_id):
    if request.user.is_superuser or request.user.is_proyectos():
        try:
            log = KpiInputData.objects.get(id=KpiInputData_id)
            serializer = CompanyKPISerializer(log)
            return JsonResponse(serializer.data)
        except KpiInputData.DoesNotExist:
            return JsonResponse({"error": "Log no encontrado"}, status=404)

#Este metodo es para reportar un log, y generara un mail a el equipo de sistemas para editar ese log
#se tienen que mostrar pruebas de el cambio, formato de solicitud a generar
#log se cambiara en la base de datos, todo menos fecha de creacion
@login_required(login_url="/login/")       
def report_log(request):
    return JsonResponse({"message": "Reportar log"})

@login_required(login_url="/login/")
def upload_excel_log(request):
    if request.user.is_superuser or request.user.is_proyectos():
        if request.method == 'POST' and request.FILES['file']:
            file = request.FILES['file']
            file_name = default_storage.save(file.name, ContentFile(file.read()))
            file_path = default_storage.path(file_name)
            
            # Procesar el archivo Excel
            df = pd.read_excel(file_path)
            
            # Aquí puedes realizar operaciones con el DataFrame df
            # Por ejemplo, guardar los datos en la base de datos
            
            return JsonResponse({"message": "Archivo subido y procesado correctamente"})
        
        return JsonResponse({"error": "No se ha subido ningún archivo"}, status=400)
    return JsonResponse({"error": "No tienes permiso para ver esta pagina"})

@login_required(login_url="/login/")
def upload_manual_log(request):
    if request.user.is_superuser or request.user.is_proyectos():
       
        if request.method == 'POST':
            data = json.loads(request.body)
            
            # Aquí puedes procesar los datos recibidos
            # Por ejemplo, guardar los datos en la base de datos
            
            return JsonResponse({"message": "Datos subidos correctamente"})
        
        return JsonResponse({"error": "No se han recibido datos"}, status=400)
    return JsonResponse({"error": "No tienes permiso para ver esta pagina"})