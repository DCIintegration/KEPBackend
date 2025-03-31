from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocumentTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import CalculatedKpi, Kpi, KpiTarget
from dashboard.utils import generate_kpi_explanation
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

@login_required(login_url="custom_auth/login/")
def download_KPI_Report(request, kpi_id):
    """
    Generate and download a PDF report for a specific KPI with AI-generated explanation
    """
    try:
        # Retrieve the KPI
        kpi = get_object_or_404(Kpi, id=kpi_id)
        
        # Check if user has permission to download the report
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You do not have permission to download this report.")
        
        # Generate AI explanation
        ai_explanation = generate_kpi_explanation(kpi)
        
        # Create a buffer for the PDF
        buffer = BytesIO()
        
        # Create the PDF document
        doc = SimpleDocumentTemplate(buffer, pagesize=letter, 
                                     rightMargin=72, leftMargin=72, 
                                     topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"KPI Report: {kpi.name}", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # KPI Details
        details = [
            ["KPI Code", kpi.code],
            ["Name", kpi.name],
            ["Description", kpi.description],
            ["Type", kpi.get_kpi_type_display()],
            ["Unit", kpi.unit or "N/A"]
        ]
        
        details_table = Table(details, colWidths=[100, 400])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.grey),
            ('TEXTCOLOR', (0,0), (0,-1), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 12))
        
        # AI-Generated Explanation
        elements.append(Paragraph("Comprehensive KPI Explanation", styles['Heading2']))
        explanation_paragraphs = ai_explanation.split('\n\n')
        for para in explanation_paragraphs:
            elements.append(Paragraph(para, styles['Normal']))
            elements.append(Spacer(1, 6))
        
        # Retrieve Calculated KPIs
        calculated_kpis = CalculatedKpi.objects.filter(kpi=kpi).order_by('-input_data__period')
        
        # KPI Calculations Table
        if calculated_kpis.exists():
            calc_data = [["Period", "Value"]]
            calc_data.extend([
                [
                    kpi_calc.input_data.period.strftime('%Y-%m-%d'), 
                    f"{kpi_calc.value} {kpi.unit}"
                ] for kpi_calc in calculated_kpis[:10]  # Limit to last 10 calculations
            ])
            
            calc_table = Table(calc_data, colWidths=[200, 200])
            calc_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            
            elements.append(Paragraph("Recent KPI Calculations", styles['Heading2']))
            elements.append(calc_table)
            elements.append(Spacer(1, 12))
        
        # Retrieve KPI Targets
        targets = KpiTarget.objects.filter(kpi=kpi).order_by('-period')
        
        if targets.exists():
            target_data = [["Period", "Target", "Min", "Max"]]
            target_data.extend([
                [
                    target.period.strftime('%Y-%m-%d'), 
                    f"{target.target_value} {kpi.unit}",
                    f"{target.min_value or 'N/A'} {kpi.unit}",
                    f"{target.max_value or 'N/A'} {kpi.unit}"
                ] for target in targets[:10]  # Limit to last 10 targets
            ])
            
            target_table = Table(target_data, colWidths=[150, 150, 100, 100])
            target_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            
            elements.append(Paragraph("KPI Targets", styles['Heading2']))
            elements.append(target_table)
        
        # Build PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer and write it to the response
        buffer.seek(0)
        response = FileResponse(
            buffer, 
            as_attachment=True, 
            filename=f"{kpi.code}_kpi_report.pdf"
        )
        
        return response
    
    except Exception as e:
        # Log the error (you might want to use Django's logging)
        print(f"Error generating KPI report: {str(e)}")
        return HttpResponseForbidden("Could not generate the report.")
