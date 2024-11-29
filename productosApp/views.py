from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm


# Verificar si es administrador
def es_admin(user):
    return user.is_authenticated and user.rol == 'admin'


# Verificar si es empleado
def es_empleado(user):
    return user.is_authenticated and user.rol in ['admin', 'empleado']


# Página principal con filtros (clientes)
def home(request):
    q = request.GET.get('q')  # Búsqueda por nombre
    categoria_id = request.GET.get('categoria')  # Filtrar por categoría
    min_precio = request.GET.get('min')  # Mínimo precio
    max_precio = request.GET.get('max')  # Máximo precio

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    # Filtros aplicados
    if q:
        productos = productos.filter(nombre__icontains=q)
    if categoria_id and categoria_id != "all":
        productos = productos.filter(categoria_id=categoria_id)

    # Validación y aplicación de filtros de precio
    try:
        if min_precio is not None and max_precio is not None:
            min_precio = int(min_precio)
            max_precio = int(max_precio)
            if min_precio < 0 or max_precio < 0:
                messages.error(request, "El precio no puede ser negativo.")
            elif min_precio > max_precio:
                messages.error(request, "El precio mínimo no puede ser mayor que el precio máximo.")
            else:
                productos = productos.filter(precio__gte=min_precio, precio__lte=max_precio)
    except ValueError:
        messages.error(request, "Por favor, ingresa valores válidos para los precios.")

    return render(request, 'index.html', {'productos': productos, 'categorias': categorias})



# Gestión de productos (empleados y administradores)
@login_required
@user_passes_test(es_empleado, login_url='home')
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'es_admin': es_admin(request.user)
    })


# Crear producto (solo administradores)
@login_required
@user_passes_test(es_admin, login_url='home')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('lista_productos')
        else:
            messages.error(request, "Error al crear el producto. Asegúrate de completar todos los campos.")
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})



# Editar producto (solo administradores)
@login_required
@user_passes_test(es_admin, login_url='home')
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente.")
            return redirect('lista_productos')
        else:
            messages.error(request, "Error al actualizar el producto. Asegúrate de completar todos los campos.")
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form})



# Eliminar producto (solo administradores)
@login_required
@user_passes_test(es_admin, login_url='home')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, f"Producto '{producto.nombre}' eliminado exitosamente.")
    return redirect('lista_productos')


# Gestión de categorías (empleados y administradores)
@login_required
@user_passes_test(es_empleado, login_url='home')
def gestionar_categorias(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST' and es_admin(request.user):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente.")
            return redirect('gestionar_categorias')
        else:
            messages.error(request, "Error al crear la categoría.")
    form = CategoriaForm()
    return render(request, 'productos/gestionar_categorias.html', {
        'categorias': categorias,
        'form': form,
        'es_admin': es_admin(request.user)
    })


# Editar categoría (solo administradores)
@login_required
@user_passes_test(es_admin, login_url='home')
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada exitosamente.")
            return redirect('gestionar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'productos/editar_categoria.html', {'form': form})


# Eliminar categoría (solo administradores)
@login_required
@user_passes_test(es_admin, login_url='home')
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.success(request, "Categoría eliminada exitosamente.")
    return redirect('gestionar_categorias')
