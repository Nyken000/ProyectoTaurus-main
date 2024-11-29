from django.contrib import admin
from .models import Carrito, ItemCarrito  # Importa los modelos de pedidos

# Registra los modelos en el sitio de administración
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
