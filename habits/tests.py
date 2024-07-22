from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habits
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.user.set_password("123456")
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.habit = Habits.objects.create(
            habit_title="Убрать лишние вещи",
            user=self.user,
            action="Сделать зарядку",
            pleasant_habit=True,
            time_perform="2024-07-23T10:00:00Z",
            location="Дом",
        )

    def test_create_habit(self):
        """Test creating a habit."""
        data = {
            "habit_title": "Убрать лишние вещи",
            "location": "Дом",
            "time_perform": "2024-07-23T10:00:00Z",
            "action": "Убрать лишние вещи"
        }

        response = self.client.post('/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.count(), 2)
        self.assertTrue(Habits.objects.all().exists())

    def test_habit_list(self):
        """Test that habit list works"""
        result = {
            "count": 1,
            "next": '',
            "previous": '',
            "results": [
                {
                    "habit_title": "Бегать вечером на дорожке",
                    "location": "Дом",
                    "user": self.user.id,
                    "time_perform": "2024-07-18T22:20:14.467029Z",
                    "action": "Пробегать на дорожке 2км",
                    "pleasant_habit": False,
                    "reward": "Попить яблочный сок",
                    "periodicity": 1,
                    "duration": "00:02:00",
                    "is_published": False,
                    "associated_habit": None,
                }
            ],
        }
        response = self.client.get('/habits/', data=result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

