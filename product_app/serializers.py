from rest_framework import serializers
from .models import RATING_CHOICES, COLOR_CHOICES


class ProductAddSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=100)
    rating = serializers.ChoiceField(choices=RATING_CHOICES, required=False)
    color = serializers.ChoiceField(choices=COLOR_CHOICES, default=COLOR_CHOICES[0][0])
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    brand = serializers.CharField(min_length=3, max_length=100)
