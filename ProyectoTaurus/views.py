from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from productosApp.models import Producto  # Importar el modelo Producto

def home(request):
    # Verificar los roles del usuario autenticado
    es_admin = request.user.is_authenticated and request.user.rol == 'admin'
    es_empleado = request.user.is_authenticated and request.user.rol == 'empleado'
    es_usuario = request.user.is_authenticated and request.user.rol == 'usuario'

    # Obtener todos los productos para mostrarlos en la página principal
    productos = Producto.objects.all()

    # Renderizar la plantilla con los datos necesarios
    return render(request, 'index.html', {
        'es_admin': es_admin,
        'es_empleado': es_empleado,
        'es_usuario': es_usuario,
        'productos': productos  # Pasar los productos al contexto
    })


def buscar_productos(request):
    query = request.GET.get('q')  # Captura el término de búsqueda
    productos = Producto.objects.filter(nombre__icontains=query) if query else Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

def filtrar_por_precio(request):
    min_price = request.GET.get('min', 0)  # Obtiene el precio mínimo del formulario
    max_price = request.GET.get('max', 9999999)  # Obtiene el precio máximo del formulario

    try:
        min_price = int(min_price)
        max_price = int(max_price)
    except ValueError:
        min_price = 0
        max_price = 9999999

    productos = Producto.objects.filter(precio__gte=min_price, precio__lte=max_price)
    return render(request, 'index.html', {'productos': productos})