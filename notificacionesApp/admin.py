from django.contrib import admin
from .models import Notificacion  # Importa el modelo de notificaciones

# Registra el modelo en el sitio de administración
admin.site.register(Notificacion)
