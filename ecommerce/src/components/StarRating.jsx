// StarRating.jsx
//Tenemos que crear un archivo nuevo para meter el número de la valoración y los votos
import React from 'react';
import { Rating } from 'primereact/rating';

const StarRating = ({ value, count }) => {
    return (
        <div className="d-flex align-items-center">
            <Rating value={value} readOnly cancel={false} style={{ margin: '15px' }} />
            <span>{value.toFixed(1)} ({count})</span>
        </div>
    );
};

export default StarRating;
