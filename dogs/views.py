from django.db.models import Avg, Count, OuterRef, Subquery
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Dog, Breed
from .serializers import DogSerializer, BreedSerializer


class DogViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки запросов к модели Dog.

    Методы:
        list: Возвращает список собак с информацией о среднем возрасте собак той же породы.
        retrieve: Возвращает детальную информацию о собаке с количеством собак той же породы.
        create, update, destroy: Стандартные методы для создания, модификации и удаления записи.
    """
    serializer_class = DogSerializer

    def get_queryser(self):
        #Базовый queryset
        queryset = Dog.objects.all()
        #для списка - аннотируем средний возраст собак для породы данной записи
        if self.action == 'list':
            avg_age_subquery = Dog.objects.filter(
                breed_id=OuterRef('breed_id')
            ).values('breed_id').annotate(avg_age=Avg('age')).values('avg_age')
            queryset = queryset.annotate(average_age=Subquery(avg_age_subquery[:1]))
        elif self.action == 'retrieve':
            count_subquery = Dog.objects.filter(
                breed_id=OuterRef('breed_id')
            ).values('breed_id').annotate(count=Count('id')).values('count')
            queryset = queryset.annotate(same_breed_count = Subquery(count_subquery[:1]))
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        '''Переопределяем retrieve для обеспечения аннотации same_breed_count.'''
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class BreedViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки запросов к модели Dog.

    Методы:
        list: Возвращает список собак с информацией о среднем возрасте собак той же породы.
        retrieve: Возвращает детальную информацию о собаке с количеством собак той же породы.
        create, update, destroy: Стандартные методы для создания, модификации и удаления записи.
    """
    serializer_class = BreedSerializer

    def get_queryset(self):
        queryset = Breed.objects.all().annotate(
            dog_count=Count('dogs')
        )
        return queryset