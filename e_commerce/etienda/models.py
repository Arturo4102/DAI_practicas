from pydantic import BaseModel, Field, validator
from .Seed import insertadatos
from typing import Any
from django.contrib import messages
from pymongo import MongoClient
import logging
from bson.objectid import ObjectId


logger = logging.getLogger(__name__)


class Nota(BaseModel):
    rate: float = Field(ge=0.0, lt=5.1, default=1)
    count: int = Field(ge=1, default=50)


class Producto(BaseModel):
    id: Any
    title: str
    price: float
    description: str
    category: str
    image: str | None
    rating: Nota

# Validador de que el título del producto deba empezar por mayúscula

    # @field_validator('title')
    @validator('title')  # Lo cambiamos porque ninja no permite
    @classmethod
    def title_mayuscula(cls, titulo):
        if titulo[0].islower():
            raise ValueError('\nEl título debe empezar por letra mayúscula')
        return titulo.title()


client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección
compras_collection = tienda_db.compras  # Colección


print("\n\nEn la BD hay: " + str(compras_collection.count_documents({})) +
      " productos insertados.\n")

print("\nEn la BD hay: " +
      str(productos_collection.count_documents({})) + " compras insertadas.\n")

#  Imprimir un producto y una compra
if productos_collection.count_documents({}):
    print("\nEjemplo de Producto:")
    print(productos_collection.find_one())

if compras_collection.count_documents({}):
    print("\nEjemplo de Compra:")
    print(compras_collection.find_one())

# Insertamos desde Seed (la primera vez solo)
# insertadatos()

# Función auxiliar que cambia el campo _id (predeterminado de MongoDB) a id (que usamos nosotros en el productos_collection)


def cambiarID(productos):
    try:
        productos = list(productos)
        for prod in productos:
            prod["id"] = str(prod.get("_id"))
            del prod["_id"]
        return productos

    except Exception as e:
        logger.error(f"Error al cambiar de _id a id de los productos %s" % (e))
        return False


# Crea una instancia del producto, la inserta en productos_collection y lo busca en productos_collection para cambiarle el _id por id
def CrearProducto(producto):
    try:
        prod_insertado = productos_collection.insert_one(producto.dict())
        prod_cambio = productos_collection.find(
            {"_id": prod_insertado.inserted_id})
        return cambiarID(prod_cambio)

    except Exception as e:
        logger.error(e)
        logger.error("Error al crear el producto")
        return False


# Función que sirve para insertar un producto en la base de datos


def InsertarProducto(request, producto_dict):
    try:
        # Convertir el objeto Nota a un diccionario antes de la inserción
        producto_dict['rating'] = producto_dict['rating'].dict()

        productos_collection.insert_one(producto_dict)
    except Exception as e:
        messages.error(
            request, f"Error al añadir el producto a la lista %s" % (e))
        logger.error(f"Error al insertar el producto %s" % (e))


# Obtiene todos los productos y cambia los _id por id

def ObtenerProductos():
    try:
        productos = productos_collection.find()
        return cambiarID(productos)

    except Exception as e:
        logger.error(f"Error al obtener los productos   %s" % (e))

        return False


# Obtiene un producto por id


def ObtenerProductosId(id):
    try:
        resultado = productos_collection.find_one({"_id": ObjectId(id)})
        return cambiarID([resultado]) if resultado else []

    except Exception as e:
        logger.error(f"Error al obtener un producto mediante su id  %s" % (e))
        return []


# Función que filtra los productos que tengan un título
# o una descripción que coincida con la búsqueda

def BusquedaProd(producto):

    resultado = productos_collection.find(
        {"$or": [{"title": {"$regex": producto, "$options": "i"}}, {"description": {"$regex": producto, "$options": "i"}}]})

    return cambiarID(resultado)

# Función que filtra los productos que sean de la categoría designada


def BusquedaCat(categoria):
    resultado = productos_collection.find({"category": categoria})

    return cambiarID(resultado)


# Modifica un atributo de un producto identificado por su id por un valor pasado


def ModificarProducto(id, atributo, valor):
    try:
        productos_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {atributo: valor}})
        return True

    except Exception as e:
        logger.error(f"Error al modificar el producto%s" % (e))

        return False

# Eliminar producto según su id


def EliminarProducto(id):
    try:
        producto = productos_collection.find_one_and_delete(
            {"_id": ObjectId(id)})
        if producto:
            # Convert the result to a ProductSchema
            return Producto(**producto)

        raise ValueError("Producto no encontrado")

    except Exception as e:
        logger.error(f"Error al eliminar el producto%s" % (e))
        return False


def ModificarRating(id, rate):
    try:
        product = productos_collection.find_one({"_id": ObjectId(id)})
        if product:
            new_rating = Nota(**product["rating"])
            new_count = new_rating.count + 1
            new_rate = ((new_rating.rate * new_rating.count) +
                        (rate * 1.0)) / new_count

            # Actualizar el rating en la colección
            productos_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"rating": {"count": new_count, "rate": new_rate}}}
            )

            # Obtener el producto modificado después de la actualización
            producto_modificado = productos_collection.find_one(
                {"_id": ObjectId(id)})
            return cambiarID([producto_modificado]) if producto_modificado else []

    except Exception as e:
        logger.error(f"Error al modificar el rating: {e}")
        return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CONSULTAS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Electrónica entre 100 y 200€, ordenados por precio

def seleccion_oferta(num):
    switch_dict = {
        1: consulta1,
        2: consulta2,
        3: consulta3
    }

    # Obtener la función correspondiente al valor del caso
    selected_case = switch_dict.get(num, consulta4)

    # Ejecutar la función seleccionada y devolver el resultado
    return selected_case()


def consulta1():

    # Usamos el $lte para el menor o igual que y $gte para el mayor o igual que
    resultado = productos_collection.find({"category": "electronics", "price": {
                                          "$gte": 100, "$lte": 200}}).sort("price", -1)
    return cambiarID(resultado)


# Productos que contengan la palabra 'pocket' en la descripción
def consulta2():

    # Usamos el $regex para buscar expresiones con un patrón específico
    resultado = productos_collection.find(
        {"description": {"$regex": "pocket", "$options": "i"}})
    return cambiarID(resultado)


# Productos con puntuación mayor de 4
def consulta3():
    # Usamos el $gt para decir mayor que
    resultado = productos_collection.find({"rating.rate": {"$gt": 4}})
    return cambiarID(resultado)

# Ropa de hombre, ordenada por puntuación


def consulta4():
    # Añadimos el -1 para realizar el orden de mayor a menor
    resultado = productos_collection.find(
        {"category": "men's clothing"}).sort("rating.rate", -1)
    return cambiarID(resultado)

# Estas consultas no las podemos poner en las ofertas porque son relativas a la facturación

# # Facturación total
# def consulta5():

#     facturacion = 0.0
#     for comp in compras_collection.find():
#         products_list = comp.get("products")
#         for prod in products_list:

#             for p in productos_collection.find():
#                 if (prod.get("productId") == p.get("id")):
#                     facturacion += p.get("price") * prod.get("quantity")

#     # Redondeamos a 2 decimales porque sale 4691.2699999999995
#     resultado = round(facturacion, 2)
#     return resultado


# def ObtenerCategorias():
#     categoria = []
#     for p in productos_collection.find():
#         se_encuentra = False
#         for cat in categoria:
#             if (cat == p.get("category") and se_encuentra == False):
#                 se_encuentra = True
#         if (se_encuentra == False):
#             categoria.append(p.get("category"))
#     return categoria

# # Facturación por categoría de producto


# def consulta6():
#     # Metemos en un array las diferentes categorías existentes para usarlas luego en la facturación
#     categoria = ObtenerCategorias()

#     # Creamos un array para meter la facturación de las categorías según la posición dentro del array categoria
#     i = 0
#     facturacion_cat = []
#     while i < categoria.__len__():
#         facturacion_cat.append(0.0)
#         i += 1

#     # Buscamos dentro de la lista de productos que tiene cada compra

#     for comp in compras_collection.find():
#         products_list = comp.get("products")
#         for prod in products_list:
#             # Y buscamos los precios dentro de la base de datos de los productos y
#             # hacemos coincidir el nombre de la categoría con la posición dentro del array de categoría
#             for cat in categoria:
#                 for p in productos_collection.find():
#                     if (prod.get("productId") == p.get("id") and cat == p.get("category")):
#                         facturacion_cat[categoria.index(
#                             cat)] += p.get("price") * prod.get("quantity")

#     resultado = facturacion_cat
#     return resultado
