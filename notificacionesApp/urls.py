from django.urls import path
from . import views 

urlpatterns = [
    path('crear/', views.crear_notificacion, name='crear_notificacion'),
    path('lista/', views.lista_notificaciones, name='lista_notificaciones'),
]
