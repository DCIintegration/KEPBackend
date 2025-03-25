from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from custom_auth.models import Empleado, Departamento
import json

# Vista para crear usuarios (solo superusuario)s
@csrf_exempt
@login_required(login_url="/login/")
def create_user(request):
    if not request.user.is_superuser:
        return JsonResponse({"error": "No tienes permisos para crear usuarios"}, status=403)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            departamento = get_object_or_404(Departamento, id=data.get("departamento")) if data.get("departamento") else None

            empleado, created = Empleado.objects.get_or_create(
                email=data["email"],
                defaults={
                    "nombre": data["nombre"],
                    "role": data["role"],
                    "puesto": data["puesto"],
                    "fecha_contratacion": data["fecha_contratacion"],
                    "activo": data.get("activo", True),
                    "sueldo": data["sueldo"],
                    "departamento": departamento,
                    "facturable": data.get("facturable", False),
                }
            )
            if created:
                return JsonResponse({"message": f"Usuario {empleado.nombre} creado correctamente"})
            else:
                return JsonResponse({"error": "El usuario ya existe"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

# Vista para eliminar usuarios (solo superusuario)
@login_required(login_url="/login/")
def delete_user(request, empleado_id):
    if request.user.is_superuser:
        empleado = get_object_or_404(Empleado, id=empleado_id)
        empleado.delete()
        return JsonResponse({"message": f"Usuario {empleado.nombre} eliminado correctamente"})
    return JsonResponse({"error": "No tienes permisos para eliminar usuarios"}, status=403)

# Vista para actualizar usuario (solo superusuario)
@csrf_exempt
@login_required(login_url="/login/")
def update_user(request, empleado_id):
    if not request.user.is_superuser:
        return JsonResponse({"error": "No tienes permisos para actualizar usuarios"}, status=403)
    
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

# Vista para visualizar todos los usuarios (solo superusuario)
@login_required(login_url="/login/")
def view_users(request):
    if request.user.is_superuser:
        empleados = list(Empleado.objects.values("id", "nombre", "role", "activo", "departamento__nombre", "profile_picture", "email"))
        return JsonResponse({"Empleados": empleados})
    
    return JsonResponse({"error": "No tienes permisos para visualizar esta información"}, status=403)


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"error": "Email y contraseña son obligatorios"}, status=400)

            user = authenticate(request, username=email, password=password)

            if user is not None:
                if not user.activo:
                    return JsonResponse({"error": "Tu cuenta está desactivada"}, status=403)
                if not user.is_email_verified:
                    return JsonResponse({"error": "Debes verificar tu correo"}, status=403)
                
                login(request, user)
                return JsonResponse({"message": "Inicio de sesión exitoso", "user": {"nombre": user.nombre, "role": user.role, "email": user.email}})
            
            return JsonResponse({"error": "Credenciales incorrectas"}, status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)
