from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Breed, Dog

class BreedAPITests(APITestCase):
    def setUp(self):
        self.breed_data = {
            "name": "Golden Retriever",
            "size": "Large",
            "friendliness": 5,
            "trainability": 5,
            "shedding_amount": 4,
            "exercise_needs": 5,
        }
        self.breed = Breed.objects.create(**self.breed_data)

    def test_list_breeds(self):
        """
        Проверяем, что при запросе списка пород возвращается корректное значение dog_count.
        """
        # Создаем несколько собак для нашей породы
        Dog.objects.create(
            name="Buddy",
            age=3,
            breed=self.breed,
            gender="Male",
            color="Golden",
            favorite_food="Bone",
            favorite_toy="Ball"
        )
        Dog.objects.create(
            name="Max",
            age=4,
            breed=self.breed,
            gender="Male",
            color="Golden",
            favorite_food="Meat",
            favorite_toy="Frisbee"
        )
        url = reverse('breed-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что для нашей породы dog_count равен 2
        for item in response.data:
            if item['id'] == self.breed.id:
                self.assertEqual(item['dog_count'], 2)

    def test_retrieve_breed(self):
        """
        Проверяем получение данных конкретной породы.
        """
        url = reverse('breed-detail', args=[self.breed.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.breed_data['name'])

    def test_create_breed(self):
        """
        Проверяем создание новой породы.
        """
        new_breed = {
            "name": "Poodle",
            "size": "Small",
            "friendliness": 4,
            "trainability": 5,
            "shedding_amount": 2,
            "exercise_needs": 3,
        }
        url = reverse('breed-list')
        response = self.client.post(url, new_breed, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_breed['name'])

    def test_update_breed(self):
        """
        Проверяем обновление данных породы.
        """
        update_data = {
            "name": "Golden Retriever Updated",
            "size": "Large",
            "friendliness": 5,
            "trainability": 5,
            "shedding_amount": 4,
            "exercise_needs": 5,
        }
        url = reverse('breed-detail', args=[self.breed.id])
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_delete_breed(self):
        """
        Проверяем удаление породы.
        """
        url = reverse('breed-detail', args=[self.breed.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Убеждаемся, что запись о породе удалена
        self.assertFalse(Breed.objects.filter(id=self.breed.id).exists())

class DogAPITests(APITestCase):
    def setUp(self):
        self.breed = Breed.objects.create(
            name="Bulldog",
            size="Medium",
            friendliness=4,
            trainability=3,
            shedding_amount=3,
            exercise_needs=2
        )
        # При прямом создании через ORM передаём экземпляр Breed, а не self.breed.id
        self.dog_data = {
            "name": "Rocky",
            "age": 5,
            "breed": self.breed,  # передаём объект, а не self.breed.id
            "gender": "Male",
            "color": "White",
            "favorite_food": "Meat",
            "favorite_toy": "Bone"
        }
        self.dog = Dog.objects.create(**self.dog_data)

    def test_list_dogs(self):
        """
        Проверяем, что при запросе списка собак возвращается корректное значение average_age для породы.
        """
        # Создаем еще одну собаку той же породы через ORM
        Dog.objects.create(
            name="Charlie",
            age=3,
            breed=self.breed,  # также передаем объект Breed
            gender="Male",
            color="White",
            favorite_food="Meat",
            favorite_toy="Ball"
        )
        url = reverse('dog-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Для собаки "Rocky" ожидаем средний возраст = (5+3)/2 = 4.0
        for item in response.data:
            if item['id'] == self.dog.id:
                self.assertAlmostEqual(float(item['average_age']), 4.0, places=1)

    def test_retrieve_dog(self):
        """
        Проверяем, что при получении конкретной собаки возвращается корректное значение same_breed_count.
        """
        # Создаем еще одну собаку той же породы через ORM
        Dog.objects.create(
            name="Max",
            age=2,
            breed=self.breed,
            gender="Male",
            color="White",
            favorite_food="Meat",
            favorite_toy="Rope"
        )
        url = reverse('dog-detail', args=[self.dog.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ожидаем, что будет две собаки данной породы (self.dog и только что созданная)
        self.assertEqual(response.data['same_breed_count'], 2)

    def test_create_dog(self):
        """
        Проверяем создание новой записи о собаке через API.
        """
        # Здесь данные отправляются через API, поэтому передаем идентификатор породы
        new_dog = {
            "name": "Bella",
            "age": 4,
            "breed": self.breed.id,  # для JSON-запроса передаем id
            "gender": "Female",
            "color": "Brown",
            "favorite_food": "Chicken",
            "favorite_toy": "Frisbee"
        }
        url = reverse('dog-list')
        response = self.client.post(url, new_dog, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_dog['name'])

    def test_update_dog(self):
        """
        Проверяем обновление записи о собаке через API.
        """
        update_data = {
            "name": "Rocky Updated",
            "age": 6,
            "breed": self.breed.id,  # для JSON-запроса передаем id
            "gender": "Male",
            "color": "Black",
            "favorite_food": "Beef",
            "favorite_toy": "Chew Toy"
        }
        url = reverse('dog-detail', args=[self.dog.id])
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])
        self.assertEqual(response.data['age'], update_data['age'])

    def test_delete_dog(self):
        """
        Проверяем удаление записи о собаке через API.
        """
        url = reverse('dog-detail', args=[self.dog.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Убеждаемся, что запись удалена
        self.assertFalse(Dog.objects.filter(id=self.dog.id).exists())

