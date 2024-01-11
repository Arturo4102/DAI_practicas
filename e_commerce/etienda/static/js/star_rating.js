// star_rating.js

document.addEventListener('DOMContentLoaded', () => {
    const spanParaEstrellas = document.querySelectorAll('span.sp');

    spanParaEstrellas.forEach(element => {
        const productId = element.getAttribute('data-product-id');
        drawStars(productId, element);
        attachStarEventListeners(element);
    });

    function attachStarEventListeners(element) {
        element.querySelectorAll('.fa').forEach(star => {
            star.addEventListener('click', handleStarClick);
            star.addEventListener('mouseover', handleStarMouseover);
            star.addEventListener('mouseout', handleStarMouseout);
        });
    }

    async function handleStarClick(event) {
        const puntuacion = parseInt(event.target.dataset.index) + 1;

        // Check if parentElement is not null before accessing its attributes
        const prodIdElement = event.currentTarget.parentElement;
        if (!prodIdElement) {
            console.error('Parent element is null or undefined.');
            return;
        }

        const prodId = prodIdElement.getAttribute('data-product-id');

        try {
            const response = await fetch(`http://localhost:8000/api/products/${prodId}/${puntuacion}`, { method: 'PUT' });
            if (response.ok) {
                drawStars(prodId, prodIdElement);
            } else {
                console.error('Error al realizar PUT:', response.status);
            }
        } catch (error) {
            console.error('Error al realizar PUT:', error);
        }
    }


    function handleStarMouseover(event) {
        const index = parseInt(event.target.dataset.index);
        const stars = event.currentTarget.parentElement.querySelectorAll('.fa');

        stars.forEach((star, i) => {
            star.classList.toggle('checked', i <= index);
        });
    }

    function handleStarMouseout(event) {
        const stars = event.currentTarget.parentElement.querySelectorAll('.fa');
        stars.forEach(star => star.classList.remove('checked'));
    }
    async function drawStars(productId, element) {
        try {
            const response = await fetch(`http://localhost:8000/api/products/${productId}`);
            if (response.ok) {
                const data = await response.json();

                // Verifica si hay una propiedad 'rating' en la respuesta
                if ('rating' in data) {
                    const ratingValue = data.rating.rate;
                    const ratingCount = data.rating.count;
                    let num_star = 0;
                    let max_star = 5;

                    element.innerHTML = '';

                    for (let i = 1; i <= ratingValue; i++) {
                        element.innerHTML += `<span class="fa fa-star" data-index="${num_star}"></span>`;
                        num_star++;
                    }

                    if (ratingValue % 1 >= 0.5) {
                        element.innerHTML += `<span class="fa fa-star-half-o" data-index="${num_star}"></span>`;
                        num_star++;
                    }

                    let last_stars = max_star - num_star;
                    for (let i = 0; i < last_stars; i++) {
                        element.innerHTML += `<span class="fa fa-star-o" data-index="${num_star}"></span>`;
                        num_star++;
                    }

                    element.innerHTML += `<span class="rate">${Number((ratingValue).toFixed(1))}(${ratingCount})</span>`;

                    // Vuelve a adjuntar los event listeners después de actualizar el contenido
                    attachStarEventListeners(element);
                } else {
                    console.error(`Error en el formato de la respuesta para el producto ${productId}`);
                }
            } else {
                console.error(`Error al obtener la puntuación para el producto ${productId}`);
            }
        } catch (error) {
            console.error('Error en la solicitud fetch:', error);
        }
    }

});
