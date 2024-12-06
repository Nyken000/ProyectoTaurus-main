from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el administrador de Django
    path('', views.home, name='home'),  # Página principal (home)
    path('usuarios/', include('usuariosApp.urls')),  # URLs de usuariosApp
    path('productos/', include('productosApp.urls')),  # URLs de productosApp
    path('notificaciones/', include('notificacionesApp.urls')),  # URLs de notificacionesApp
    path('pedidos/', include('pedidosApp.urls')),  # URLs de pedidosApp
    path('buscar/', views.buscar_productos, name='buscar_productos'),  # Ruta para buscar productos
    path('filtrar/precio/', views.filtrar_por_precio, name='filtrar_por_precio'),  # Ruta para filtrar por precio
    path('', include('pedidosApp.urls')),
]

if settings.DEBUG:  # Solo en modo de depuración
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
