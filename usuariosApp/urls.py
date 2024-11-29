from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('asignar-rol/<int:user_id>/', views.asignar_rol, name='asignar_rol'),
]
