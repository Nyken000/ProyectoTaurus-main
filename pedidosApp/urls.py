from django.urls import path
from . import views
from .views import checkout_pro, pago_exitoso, pago_error, pago_pendiente

urlpatterns = [
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_item_carrito, name='eliminar_item_carrito'),
    path('actualizar-cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path("checkout-pro/", checkout_pro, name="checkout_pro"),
    path("pagos/exito/", pago_exitoso, name="pago_exitoso"),
    path("pagos/error/", pago_error, name="pago_error"),
    path("pagos/pendiente/", pago_pendiente, name="pago_pendiente"),
]
