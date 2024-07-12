from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.model import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(name="Математика")
        self.lesson = Lesson.objects.create(name="Урок_1", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "name": "Урок_10"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.filter(name="Урок_1").count(), 1
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Урок_10"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Урок_10"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "link_to_video": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        # self.user.set_password('1')
        self.course = Course.objects.create(name="Ботаника", description="Что-то про ботаников", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("materials:subscription-list")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "Subscription added"})

    def test_unsubscribe(self):
        url = reverse("materials:subscription-list")
        data = {"course": self.course.pk}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Subscription removed'})
