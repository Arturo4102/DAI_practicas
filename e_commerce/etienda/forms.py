from django import forms
from django.core.exceptions import ValidationError
import logging
from .models import Nota

logger = logging.getLogger(__name__)


def title_mayuscula(title):
    if title[0].islower():
        logger.error(
            'El título de un producto a insertar debe empezar por mayúscula')
        raise ValidationError(
            ("%(value)s debe empezar con mayúscula"),
            params={"value": title},
        )


class ProductoForm(forms.Form):
    title = forms.CharField(label='Nombre', max_length=100,
                            required=True, validators=[title_mayuscula])

    price = forms.FloatField(
        label='Precio (€)', min_value=0, required=True)

    description = forms.CharField(
        label='Descripción', widget=forms.Textarea, max_length=100, required=True)

    CATEGORY_CHOICES = [
        ('men\'s clothing', 'Ropa de hombre'),
        ('women\'s clothing', 'Ropa de mujer'),
        ('electronics', 'Electronica'),
        ('jewelery', 'Joyas'),
    ]

    category = forms.ChoiceField(
        label='Categoría', choices=CATEGORY_CHOICES, required=True)
    image = forms.FileField(label='Imágenes', required=False)

    rating_rate = forms.FloatField(
        label='Rating Rate', min_value=0., max_value=5., initial=1)
    rating_count = forms.IntegerField(
        label='Rating Count', min_value=1, initial=50)

    def clean(self):
        cleaned_data = super().clean()
        rating_rate = cleaned_data.get('rating_rate')
        rating_count = cleaned_data.get('rating_count')

        # Crear una instancia de Nota
        nota_instance = Nota(rate=rating_rate, count=rating_count)

        # Asignar la instancia de Nota a cleaned_data
        cleaned_data['rating'] = nota_instance
        return cleaned_data
