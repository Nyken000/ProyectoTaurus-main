
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('usuario', 'Usuario'),
    )
    rol = models.CharField(max_length=10, choices=ROLES)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        permissions = [
            ("can_manage_users", "Puede gestionar usuarios"),
            ("can_manage_inventory", "Puede gestionar inventario"),
            ("can_view_public_info", "Puede ver información pública"),
        ]

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
