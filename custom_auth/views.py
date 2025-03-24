from django.shortcuts import render

#Las vistas acontinuacion solo estaran disponibles para el super usuario
#vista para crear usuarios
def create_user(request):
    return

#vista para eliminar usuarios
def delete_user(request):
    return

#vista para editar usuario
def update_user(request):
    return

#Vista para visualizar usuarios
def view_users(request):
    return

#Login (Unica vista disponible para todos los usuarios)
def login(request):
    return

#Esta vista es un mail que se generara para confirmar la creacion de un nuevo usuario, usando el correo empresarial
def confirmar_usuario(request):
    return
