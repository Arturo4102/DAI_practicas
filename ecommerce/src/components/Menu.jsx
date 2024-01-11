import React from 'react';
import { Button, Container, Form, Navbar } from 'react-bootstrap';

export default function Menu({ filtrarPorTitulo, filtrarPorCategoria, categorias }) {
    return (
        <Navbar expand="lg" className="bg-body-tertiary" >
            <Container fluid>
                <Navbar.Brand href="#">Etienda</Navbar.Brand>
                <Navbar.Toggle aria-controls="navbarScroll" />
                <Navbar.Collapse id="navbarScroll">
                    <Form className="ms-auto">
                        <Form.Select
                            className="me-2"
                            aria-label="Categorías"
                            onChange={(evento) => filtrarPorCategoria(evento)}
                            id="selectCategorias"
                        >
                            <option value="">Todas las categorías</option>
                            {categorias.map((categoria, index) => (
                                <option key={index} value={categoria}>
                                    {categoria}
                                </option>
                            ))}
                        </Form.Select>
                        <Form.Control
                            type="search"
                            placeholder="Search"
                            className="me-2"
                            aria-label="Search"
                            onChange={(evento) => filtrarPorTitulo(evento)}
                        />
                        <Button variant="outline-success">Búsqueda</Button>
                    </Form>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}
