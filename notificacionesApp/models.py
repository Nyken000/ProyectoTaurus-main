from django.db import models
from usuariosApp.models import Usuario

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificaciones")
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación para {self.usuario.username} - {'Leída' if self.leida else 'No leída'}"

    class Meta:
        ordering = ['-fecha_creacion']  # Notificaciones más recientes primero
