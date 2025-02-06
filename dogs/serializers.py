from rest_framework import serializers
from .models import Dog, Breed


class BreedSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Breed'''
    dog_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = [
            'id', 'name', 'size', 'friendless', 'trainbility',
            'shedding_amount', 'exercise_needs', 'dogs_count'
        ]

class DogSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Dog'''
    #Добавляем поля для агрегатных состояний
    average_age = serializers.FloatField(read_only=True)
    same_breed_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = [
            'id', 'name', 'age', 'breed', 'gender', 'color',
            'favorite_food', 'favorite_toy', 'avarage_age', 'same_breed_count'
        ]
    