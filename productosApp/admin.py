from django.contrib import admin
from .models import Producto, Categoria  # Importa los modelos

# Registra los modelos en el sitio de administración
admin.site.register(Producto)
admin.site.register(Categoria)
