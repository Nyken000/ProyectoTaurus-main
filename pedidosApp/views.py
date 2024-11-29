import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Carrito, ItemCarrito
from productosApp.models import Producto
from math import floor
from django.http import JsonResponse


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
