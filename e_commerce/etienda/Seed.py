# Seed.py
import os
from pymongo.mongo_client import MongoClient
from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from datetime import datetime
from typing import Any
import requests

# https://requests.readthedocs.io/en/latest/


def getProductos(api):
    response = requests.get(api)
    return response.json()


# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/

class Nota(BaseModel):
    rate: float = Field(ge=0., lt=5., default=1)
    count: int = Field(ge=1, default=50)


class Producto(BaseModel):
    _id: Any
    title: str
    price: float
    description: str
    category: str
    image: str | None
    rating: Nota

    # @field_serializer('image')
    # def serializaPath(self, val) -> str:
    #     if type(val) is pathlib.PosixPath:
    #         return str(val)
    #     return val


class Compra(BaseModel):
    _id: Any
    user: EmailStr
    date: datetime
    products: list


# dato = {
    # 'title': "MBJ Women's Solid Short Sleeve Boat Neck V ",
    # 'price': 9.85,
    # 'description': '95% RAYON 5% SPANDEX, Made in USA or Imported, Do Not Bleach, Lightweight fabric with great stretch for comfort, Ribbed on sleeves and neckline / Double stitching on bottom hem', 'category': "women's clothing",
    # 'category': "women's clothing",
    # 'image': None,
    # 'rating': {'rate': 4.7, 'count': 130}
# }

# nueva_compra = {
# 'user': str('fulanito@correo.com'),
# 'date': datetime.now(),
# 'products': lista_productos_ids
# }
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección
compras_collection = tienda_db.compras  # Colección


def insertadatos():
    productos_collection.drop()
    compras_collection.drop()

    # Obtención productos de la API
    productos = getProductos('https://fakestoreapi.com/products')

    # Para que las use el servidor
    directorio_destino = "etienda/static/imagenes/"

    # Como backup
    directorio_imagenes = "/imagenes/"

    # Crear el directorio 'imagenes/' si no existe
    if not os.path.exists(directorio_imagenes):
        os.makedirs(directorio_imagenes)

    for p in productos:
        url = p.get("image")  # Descargamos Imagen
        nombre_archivo = p['image'].split('/')[-1]
        nombre_archivo_destino = directorio_imagenes+nombre_archivo
        ruta_archivo_destino = directorio_destino+nombre_archivo
        response = requests.get(url)

        with open(ruta_archivo_destino, "wb") as archivo:
            archivo.write(response.content)
        with open(nombre_archivo_destino, "wb") as archivo:
            archivo.write(response.content)
        p['image'] = nombre_archivo_destino
        p.pop('id')

        Producto(**p)

        productos_collection.insert_one(p)

    # Obtención compras de la API
    compras = getProductos('https://fakestoreapi.com/carts')

    for c in compras:
        # (Esta línea se debería comentar después del primer insertado ya que sino se insertarían de nuevo los mismos datos)
        compras_collection.insert_one(c)
