from django.contrib import admin
from .models import Inventario  # Importa el modelo de inventario (ajusta según sea necesario)

# Registra el modelo en el sitio de administración
admin.site.register(Inventario)
