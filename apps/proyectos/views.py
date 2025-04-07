import datetime
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.dashboard.models import KpiInputData
from .serializers import CompanyKPISerializer

#quiero ver la info pro la tengo que filtrar con una funcion, asi de sencillo we, tiene que haber una pantalla principal 
#que sea un registro con los diferentes logs de informacion, cada vez que se alimena con info de kpi con filtros

@login_required(login_url="custom_auth/login/")
def view_logs(request):
    if request.user.is_superuser or request.user.is_proyectos():
        info = list(KpiInputData.objects.values("created_at", "total_horas_facturables", "total_horas_planta", "total_horas_planta", "numero_empleados", "numero_empleados_facturables", "dias_trabajados", "costo_por_hora", "ganancia_total"))
        return JsonResponse(info)
        
    return JsonResponse({"error": "No tienes permiso para ver esta pagina"})

@login_required(login_url="custom_auth/login/")
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
@login_required(login_url="custom_auth/login/")      
def report_log(request, KpiInputData_id):
    if request.user.is_superuser or request.user.is_proyectos():
        try:
            log = KpiInputData.objects.get(id=KpiInputData_id)
            log.status = "reportado"
            log.save()
            #Queda pendiente logica de notificaciones via correo electronico para el equipo de sistemas
            return JsonResponse({"message": "Log reportado correctamente"})
        except KpiInputData.DoesNotExist:
            return JsonResponse({"error": "Log no encontrado"}, status=404)
    return JsonResponse({"message": "Reportar log"})

@login_required(login_url="custom_auth/login/")
def modify_log(request, KpiInputData_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            try:
                log = KpiInputData.objects.get(id=KpiInputData_id)
                data = json.loads(request.body)
                
                KpiInputData.total_horas_facturables =data.get("total_horas_facturables", log.total_horas_facturables)
                KpiInputData.total_horas_planta =data.get("total_horas_planta", log.total_horas_planta)
                KpiInputData.total_horas_facturadas =data.get("total_horas_facturadas", log.total_horas_facturadas)
                KpiInputData.numero_empleados =data.get("numero_empleados", log.numero_empleados)
                KpiInputData.numero_empleados_facturables =data.get("numero_empleados_facturables", log.numero_empleados_facturables)
                KpiInputData.dias_trabajados =data.get("dias_trabajados", log.dias_trabajados)
                KpiInputData.costo_por_hora =data.get("costo_por_hora", log.costo_por_hora)
                KpiInputData.ganancia_total =data.get("ganancia_total", log.ganancia_total)
                KpiInputData.save()
                
                return JsonResponse({"message": "Log modificado correctamente"})
            except KpiInputData.DoesNotExist:
                return JsonResponse({"error": "Log no encontrado"}, status=404)
        return JsonResponse({"message": "sin accedo"})

#Trabajar en lo que puede pasar con el modelo de KPI input data 
@login_required(login_url="custom_auth/login/")
def upload_excel_log(request):
    if request.user.is_superuser or request.user.is_proyectos():
        if request.method == 'POST' and request.FILES.get('file'):
            try:
                file = request.FILES['file']
                period_str = request.POST.get('period')
                file_type = request.POST.get('file_type', 'total')
                
                # Validar y convertir la fecha
                try:
                    if period_str:
                        period = datetime.strptime(period_str, '%Y-%m-%d').date()
                    else:
                        # Si no se proporciona una fecha, usar el primer día del mes actual
                        today = datetime.now()
                        period = datetime(today.year, today.month, 1).date()
                except ValueError:
                    return JsonResponse({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=400)
                
                # Verificar si ya existe un registro para este período y tipo de archivo
                existing = KpiInputData.objects.filter(period=period, file_type=file_type).first()
                
                if existing:
                    # Actualizar registro existente
                    existing.raw_data_file.delete(save=False)  # Eliminar archivo antiguo
                    existing.raw_data_file = file
                    existing.save()
                    kpi_data = existing
                else:
                    # Crear nuevo registro
                    kpi_data = KpiInputData(
                        period=period,
                        file_type=file_type,
                        raw_data_file=file
                    )
                    kpi_data.save()
                
                # Calcular KPIs si se tienen todos los datos necesarios
                kpi_results = kpi_data.calcular_kpis()
                
                response_data = {
                    "message": "Archivo subido y procesado correctamente",
                    "id": kpi_data.id,
                    "period": period.strftime('%Y-%m-%d'),
                    "file_type": kpi_data.get_file_type_display(),
                    "total_horas_facturables": kpi_data.total_horas_facturables,
                    "total_horas_planta": kpi_data.total_horas_planta,
                    "numero_empleados": kpi_data.numero_empleados
                }
                
                if kpi_results:
                    response_data["kpis"] = kpi_results
                
                return JsonResponse(response_data)
                
            except Exception as e:
                
                return JsonResponse({
                    "error": f"Error al procesar el archivo: {str(e)}"
                }, status=500)
        
        # Si es GET o no hay archivo, devolver formulario o mensaje
        return JsonResponse({"error": "No se ha subido ningún archivo"}, status=400)
    
    return JsonResponse({"error": "No tienes permiso para ver esta página"}, status=403)

@login_required(login_url="custom_auth/login/")
def upload_manual_log(request):
    if request.user.is_superuser or request.user.is_proyectos():
       
        if request.method == 'POST':

            try:
                data = json.loads(request.body)

                KpiInputData , created = KpiInputData.objects.get_or_create(
                    defaults={
                        "total_horas_facturables": data["total_horas_facturables"],
                        "total_horas_planta": data["total_horas_planta"],
                        "total_horas_facturadas": data["total_horas_facturadas"],
                        "numero_empleados": data["numero_empleados"],
                        "numero_empleados_facturables": data["numero_empleados_facturables"],
                        "dias_trabajados": data["dias_trabajados"],
                        "costo_por_hora": data["costo_por_hora"],
                        "ganancia_total": data["ganancia_total"],
                    }
                )
                if created:
                    return JsonResponse({"message": f"Log {KpiInputData} creado exitosamente"})
                else:
                    return JsonResponse({"error": "Este log ya existe"}, status=400)
                
            except json.JSONDecodeError:
                return JsonResponse({"error": "Error al decodificar el JSON"}, status=400)
     
        return JsonResponse({"error": "No se han recibido datos"}, status=400)
    return JsonResponse({"error": "No tienes permiso para ver esta pagina"})