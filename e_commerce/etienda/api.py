from ninja_extra import NinjaExtraAPI
from ninja import Schema, Query, Form

import logging
from etienda import models
from typing import List


logger = logging.getLogger(__name__)


api = NinjaExtraAPI()


class Rate(Schema):
    rate: float
    count: int


class ProductSchema(Schema):  # sirve para validar y para documentación
    id:    str
    title: str
    price: float
    description: str
    category: str
    image: str = None
    rating: Rate = None


class ProductSchemaIn(Schema):
    title: str
    price: float
    description: str
    category: str
    rating: Rate


class ErrorSchema(Schema):
    message: str


# Buscar 4 Productos
@api.get('/products', response={202: List[ProductSchema]})
def Productos(request, since: int = Query(default=0), to: int = Query(default=4)):
    resultados = models.ObtenerProductos()[since:to]
    return 202, list(resultados)


@api.get('/products/{id}', response={200: ProductSchema, 404: ErrorSchema})
def ProductosId(request, id: str):
    try:
        resultado = models.ObtenerProductosId(id)
        return 200, resultado[0]

    except Exception as e:
        return 404, {"message": f"No se ha encontrado el producto    %s" % (e)}


@api.put("/productos/{id}", response={202: ProductSchema, 404: ErrorSchema})
def Modifica_producto(request, id: str, payload: ProductSchemaIn):
    try:
        for attr, value in payload.dict().items():
            logger.debug(f'{attr} -> {value}')
            models.ModificarProducto(id, attr, value)
        payload["id"] = id

        logger.debug(f'{payload}')
        return 202, {'message': f'Modificación hecha %s' % (payload)}
    except:
        return 404, {'message': 'no encontrado'}


@api.delete('/products/{id}', response={200: ProductSchema, 404: ErrorSchema})
def EliminarProducto(request, id: str):
    try:
        producto = models.EliminarProducto(id)

        return 200, producto

    except Exception as e:
        logger.error(e)

        return 404, {"message": f"No se ha encontrado el producto   %s" % (e)}


@api.post('/products', response={201: ProductSchema, 400: ErrorSchema})
def CrearProducto(request, payload: ProductSchemaIn):
    try:
        id_prod_creado = models.CrearProducto(payload)

        if id_prod_creado:
            # If product creation is successful, retrieve the product details
            prod_creado = models.ObtenerProductosId(id_prod_creado)
            return 201, prod_creado[0]
        else:
            # Handle the case where product creation fails
            return 400, {"message": "No se ha podido crear el producto"}

    except Exception as e:
        logger.error(e)
        return 400, {"message": "No se ha podido crear el producto"}


# # Método para autenticación en la API, donde se comprueban las credenciales de un usuario y se devuelve un token
@api.post("/token", auth=None)
def get_token(request, username: str = Form(...), password: str = Form(...)):
    if username == "arturo4102" and password == "practicas,DAI":
        return {"token": "USER_ADMIN"}
    else:
        return {"message": "Error en la autenticación"}


@api.put('/products/{id}/{rating}', response={202: List[ProductSchema], 404: ErrorSchema})
def ModificarRating(request, id: str, rating: int):
    try:
        logger.debug(
            f'Modificando rating para el producto {id} con {rating} estrellas.')
        resultado = models.ModificarRating(id, rating)
        return 202, list(resultado)
    except Exception as e:
        logger.error(
            f'Error al modificar el rating para el producto {id}: {e}')
        return 404, {"message": f"No se ha encontrado el producto {id}"}
