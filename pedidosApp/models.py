from django.db import models
from usuariosApp.models import Usuario  # Importar el modelo de usuario
from productosApp.models import Producto
from math import floor
class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carrito')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.total_item() for item in self.items.all())
    
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def total_item(self):
        return self.producto.precio * self.cantidad
