import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Carrito, ItemCarrito
from productosApp.models import Producto
from math import floor
from django.http import JsonResponse
from django.conf import settings
import mercadopago

@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = sum(floor(item.total_item()) for item in items)
    return render(request, 'pedidos/ver_carrito.html', {
        'carrito': carrito,
        'items': items,
        'total': total,
        'es_admin': request.user.rol == 'admin'
    })


@login_required
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Verifica que el producto tenga stock
    if producto.stock <= 0:
        messages.error(request, f"El producto '{producto.nombre}' no está disponible porque no tiene stock.")
        return redirect('home')

    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    item, item_creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not item_creado:
        item.cantidad += 1
        item.save()
    messages.success(request, f"'{producto.nombre}' ha sido añadido al carrito.")
    return redirect('ver_carrito')


@login_required
def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, "El producto ha sido eliminado del carrito.")
    return redirect('ver_carrito')


@login_required
def actualizar_cantidad(request, item_id):
    if request.method == 'POST':
        try:
            # Depuración inicial para asegurar que request.body tiene contenido válido
            print("Request Body: ", request.body)

            item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
            data = json.loads(request.body)  # Intentamos cargar el JSON

            nueva_cantidad = int(data.get('cantidad', 1))
            item.cantidad = nueva_cantidad
            item.save()

            # Calcula el nuevo subtotal y total
            subtotal = item.total_item()
            carrito = item.carrito
            total = sum(i.total_item() for i in carrito.items.all())

            return JsonResponse({
                'success': True,
                'subtotal': subtotal,
                'total': total
            })
        except Exception as e:
            # Registrar el error para mayor visibilidad
            print("Error during actualizar_cantidad: ", str(e))
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})



@login_required
def checkout_pro(request):
    try:
        # SDK de Mercado Pago
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

        # Obtener el carrito del usuario
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if not carrito or not carrito.items.exists():
            messages.error(request, "Tu carrito está vacío.")
            return redirect('ver_carrito')

        # Crear preferencia de pago
        preference_data = {
            "items": [
                {
                    "title": item.producto.nombre,
                    "quantity": item.cantidad,
                    "currency_id": "CLP",
                    "unit_price": float(item.producto.precio),
                }
                for item in carrito.items.all()
            ],
            "payer": {
                "email": request.user.email,
            },
            "back_urls": {
                "success": request.build_absolute_uri("/pedidos/pagos/exito/"),
                "failure": request.build_absolute_uri("/pedidos/pagos/error/"),
                "pending": request.build_absolute_uri("/pedidos/pagos/pendiente/"),
            },
            "auto_return": "approved",
        }

        # Llamar al SDK para crear la preferencia
        response = sdk.preference().create(preference_data)
        preference = response.get("response", {})

        # Redirigir al cliente al init_point de Mercado Pago
        if "init_point" in preference:
            return redirect(preference["init_point"])
        else:
            messages.error(request, "No se pudo generar el enlace de pago.")
            return redirect('ver_carrito')
    except Exception as e:
        print(f"Error en checkout_pro: {e}")
        messages.error(request, "Ocurrió un error al procesar el pago.")
        return redirect('ver_carrito')



def pago_exitoso(request):
    return render(request, "pagos/exito.html")

def pago_error(request):
    return render(request, "pagos/error.html")

def pago_pendiente(request):
    return render(request, "pagos/pendiente.html")
