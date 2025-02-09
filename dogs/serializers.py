from rest_framework import serializers
from .models import Breed, Dog

class BreedSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Breed."""
    dog_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = [
            'id', 
            'name', 
            'size', 
            'friendliness',
            'trainability', 
            'shedding_amount', 
            'exercise_needs',
            'dog_count',
        ]


class DogSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Dog."""
    # Дополнительные поля для агрегированных данных
    average_age = serializers.FloatField(read_only=True)
    same_breed_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = [
            'id',
            'name',
            'age',
            'breed',
            'gender',
            'color',
            'favorite_food',
            'favorite_toy',
            'average_age',       
            'same_breed_count',  
        ]
