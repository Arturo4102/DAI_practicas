import os
import random
import logging
from django.shortcuts import render, redirect
from Ecommerce.settings import BASE_DIR
from .forms import ProductoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BusquedaProd, BusquedaCat, InsertarProducto, seleccion_oferta

# Hacemos uso del logger para tener el registro de eventos
logger = logging.getLogger(__name__)

# Página principal con ofertas


def index(request):

    # hasta índice 3 porque hay 4 consultas
    productos = seleccion_oferta(random.randint(0, 3))

    return render(request, 'index.html', {'productos': productos})

# Obtiene los productos que coincidan con los términos de la barra de búsqueda


def buscar_producto(request):
    # Obtenemos el valor del campo de búsqueda desde la solicitud GET
    productos = BusquedaProd(request.GET.get('producto', ''))

    return render(request, 'buscar_producto.html', {'productos': productos})


# Obtiene los productos seleccionado desde el menú desplegable de Categorias


def buscar_categoria(request, categoria):
    productos = BusquedaCat(categoria)
    return render(request, 'buscar_categoria.html', {'productos': productos, 'categoria': categoria})

# Definición de la vista para el formulario de añadir un nuevo producto


@login_required  # Necesitamos que esté logeado el usuario y tenga los permisos
def nuevo_producto(request):
    logger.debug("Este es un mensaje de depuración")
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES)

        if producto_form.is_valid():
            producto_dict = {
                'title': producto_form.cleaned_data['title'],
                'price': producto_form.cleaned_data['price'],
                'description': producto_form.cleaned_data['description'],
                'category': producto_form.cleaned_data['category'],
                'image': None,
                'rating': producto_form.cleaned_data['rating'],
            }

            ruta = None

            if producto_form.cleaned_data['image'] != None:
                ruta = os.path.join(BASE_DIR, 'etienda/static/imagenes',
                                    producto_form.cleaned_data['image'].name)
                ruta_enlace = os.path.join('imagenes',
                                           producto_form.cleaned_data['image'].name)
            try:
                with open(ruta, 'wb') as ruta_imagen:
                    for chunk in producto_form.cleaned_data['image'].chunks():
                        ruta_imagen.write(chunk)

            except Exception as e:
                messages.error(request, f"Error al escribir el archivo: {e}")
                logger.error('Error añadiendo un producto')
            logger.info("Este es un mensaje de información")
            producto_dict['image'] = ruta_enlace

            InsertarProducto(request, producto_dict)
            return redirect('index')

        else:
            messages.error(request, "Error del formulario")
            logger.error('Error añadiendo un producto')

    else:
        producto_form = ProductoForm()
    return render(request, 'nuevo_prod.html', {'producto_form': producto_form})
