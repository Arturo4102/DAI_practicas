import React from 'react';
import { Button, Card, Col, Row } from 'react-bootstrap';
import StarRating from './StarRating';

export default function Resultados({ productos }) {
    return (
        <Row xs={1} sm={1} md={2} lg={3} xl={4} className="g-4">
            {productos.map((producto) => (
                <Col key={producto.id}>
                    <Card>
                        <Card.Img variant="top" src={`src/${producto.image}`}
                            style={{
                                objectFit: 'cover',
                                borderRadius: '8px',
                                margin: '0 auto',
                                display: 'block',
                                maxWidth: '200px',
                                height: 'auto'
                            }} />
                        <Card.Body>
                            <Card.Title>{producto.title}</Card.Title>
                            <Card.Text>{producto.description}</Card.Text>
                        </Card.Body>
                        <div className="d-flex justify-content-center align-items-center">
                            <StarRating value={producto.rating.rate} count={producto.rating.count} />

                        </div>

                        <Card.Footer className="d-flex justify-content-between align-items-center">
                            <Button variant="primary">Comprar</Button>
                            <p className="m-0">{producto.price} €</p>
                        </Card.Footer>
                    </Card>
                </Col>
            ))}
        </Row>
    );
}
