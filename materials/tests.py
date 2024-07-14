from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.model import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(name="Математика")
        self.lesson = Lesson.objects.create(
            name="Урок_1", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {"name": "Урок_10"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.filter(name="Урок_1").count(), 1)

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"name": "Урок_10"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок_10")

    def test_lesson_delete(self):
        url = reverse("materials:lesson_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        # print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # result = {
        #     "count": 1,
        #     "next": None,
        #     "previous": None,
        #     "results":
        result = [
            {
                "id": self.lesson.pk,
                "name": self.lesson.name,
                "description": self.lesson.description,
                "image_ph": None,
                "link_to_video": None,
                "course": self.course.pk,
                "owner": self.user.pk,
            }
        ]

        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email="admin@example.com", password="123qwe")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="test", owner=self.user)
        self.subscription = Subscription.objects.create(
            course=self.course, user=self.user
        )

    def test_create_subscription(self):
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }

        response = self.client.post(reverse("materials:subscription"), data=data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json(), "подписка удалена")
