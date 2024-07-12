from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.model import Course, Lesson, Subscription
from users.models import User


class TestLessons(APITestCase):
    """ Тестирование уроков """

    def setUp(self) -> None:
        self.user = User.objects.create(email="admin@example.com")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="Python", description="Основы Python")
        self.lesson = Lesson.objects.create(
            name="Исключения",
            course=self.course,
            description="Разновидности Исключений",
            link_to_video="https://www.youtube.com/watch",
            owner=self.user,
        )

    def test_create_lesson(self):
        """ Тестирование создания урока """

        url = reverse("materials:lesson_create")
        data = {
            "name": "Исключения",
            "description": "Разновидности Исключений",
            "course": self.lesson.course.id,
            "link_to_video": "https://www.youtube.com/watch",
        }

        response = self.client.post(url, data=data)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(data.get("name"), "Исключения")
        self.assertEqual(data.get("course"), self.lesson.course.id)
        self.assertEqual(data.get("link_to_video"), "https://www.youtube.com/watch")
        self.assertEqual(data.get("description"), "Разновидности Исключений")

    def test_update_lesson(self):
        """ Тестирование изменений урока """

        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Исключения",
            "description": "Виды Исключений",
            "course": self.lesson.course.id,
            "link_to_video": "https://www.youtube.com/watch",
        }
        response = self.client.put(url, data)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)
        self.assertEqual(data.get("description"), "Виды Исключений")
        self.assertEqual(data.get("course"), self.lesson.course.id)
        self.assertEqual(data.get("owner"), self.lesson.owner.id)

    def test_list_lesson(self):
        """ Тестирование списка уроков """

        url = reverse("materials:lesson_list")
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.id,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "link_to_video": self.lesson.link_to_video,
                    "course": self.lesson.course.id,
                    "owner": self.lesson.owner.id,
                },
            ],
        }
        response = self.client.get(url)

        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_retrieve_lesson(self):
        """ Тестирование просмотра одного урока """

        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)
        self.assertEqual(data.get("description"), self.lesson.description)
        self.assertEqual(data.get("course"), self.lesson.course.id)
        self.assertEqual(data.get("owner"), self.lesson.owner.id)

    def test_delete_lesson(self):
        url = reverse("materials:lesson_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):
    """ Тестирование подписок """

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(name="Python", description="Основы Python")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("materials:subscription-list")

    def test_subscription_activate(self):
        """Тестирование активации подписки"""
        data = {"user": self.user.id, "course": self.course.id}
        response = self.client.post(self.url, data=data)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.all().count(), 1)
        self.assertEqual(
            Subscription.objects.filter(user=self.user, course=self.course).exists(),
            True,
        )
        self.assertEqual(response.json().get("message"), "подписка добавлена")

    def test_subscription_deactivate(self):
        """ Тестирование деактивации подписки """

        data = {"user": self.user.id, "course": self.course.id}
        response = self.client.post(self.url, data=data)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.all().count(), 0)
        self.assertEqual(response.json().get("message"), "подписка удалена")
