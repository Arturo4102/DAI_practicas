// App.jsx
import React, { useState, useEffect } from 'react';
// import './css/App.css';
import Menu from './components/Menu';
import Resultados from './components/Resultados';

const API_URL = "http://localhost:8000/api/products";
const PRODUCTS_RANGE = "?since=0&to=30";

function App() {
  const [productos, setProductos] = useState([]);
  const [productos_Filt, setProductos_Filt] = useState([]);
  const [categorias, setCategorias] = useState([]);

  const filtrarPorTitulo = (evento) => {
    const valorBusqueda = evento.target.value.toLowerCase(); //Lo hacemos insensible a mayuscula y a minuscula

    if (valorBusqueda !== "") {
      const productosFiltrados = productos.filter((producto) => producto.title.toLowerCase().includes(valorBusqueda));
      setProductos_Filt(productosFiltrados);
    } else {
      setProductos_Filt(productos);
    }

    console.log(valorBusqueda);
  }

  const filtrarPorCategoria = (evento) => {
    const valorBusqueda = evento.target.value.toLowerCase();  //Lo hacemos insensible a mayuscula y a minuscula

    if (valorBusqueda !== "") {
      const productosFiltrados = productos.filter((producto) => producto.category.toLowerCase().includes(valorBusqueda));
      setProductos_Filt(productosFiltrados);
    } else {
      setProductos_Filt(productos);
    }

    console.log(valorBusqueda);
  }

  useEffect(() => {
    fetch(`${API_URL}${PRODUCTS_RANGE}`)  //llamada a la API, el resultado es una Promise
      .then((response) => response.json()) //cuando la petición finalice, transformamos la respuesta a JSON (response.json() también es una Promise)
      .then((prods) => {     //aquí vamos a trabajar y modificar la respuesta después de que está ya convertida en JSON
        setProductos(prods);
        const uniqueCategorias = Array.from(new Set(prods.map((producto) => producto.category)));
        setCategorias(uniqueCategorias);
        setProductos_Filt(prods);
      });
  }, []);


  return (
    <>
      <Menu filtrarPorTitulo={filtrarPorTitulo} categorias={categorias} filtrarPorCategoria={filtrarPorCategoria} />
      <Resultados productos={productos_Filt} />
    </>
  );
}

export default App;


