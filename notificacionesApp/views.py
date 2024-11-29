from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Notificacion
from usuariosApp.models import Usuario  # Asegúrate de importar el modelo Usuario

def crear_notificacion(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')  # Obtén el ID del usuario
        mensaje = request.POST.get('mensaje')       # Obtén el mensaje de la notificación

        if not usuario_id or not mensaje:
            messages.error(request, "Debes completar todos los campos.")
            return redirect('crear_notificacion')  # Redirige al formulario nuevamente

        try:
            usuario = Usuario.objects.get(id=usuario_id)
            Notificacion.objects.create(usuario=usuario, mensaje=mensaje)
            messages.success(request, "Notificación creada correctamente.")
            return redirect('lista_notificaciones')  # Redirige a la lista de notificaciones
        except Usuario.DoesNotExist:
            messages.error(request, "El usuario no existe.")
            return redirect('crear_notificacion')

    usuarios = Usuario.objects.all()
    return render(request, 'notificaciones/crear_notificacion.html', {'usuarios': usuarios})

def lista_notificaciones(request):
    notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')
    return render(request, 'notificaciones/lista_notificaciones.html', {
        'notificaciones': notificaciones,
        'es_admin': request.user.rol == 'admin'
    })