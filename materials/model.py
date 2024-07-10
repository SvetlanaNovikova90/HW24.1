from django.conf import settings
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    image_ph = models.ImageField(
        upload_to="materials/photo", **NULLABLE, verbose_name="Изображение"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    image_ph = models.ImageField(
        upload_to="materials/photo", **NULLABLE, verbose_name="Изображение"
    )
    course = models.ForeignKey(
        Course,
        **NULLABLE,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
    )
    link_to_video = models.TextField(**NULLABLE, verbose_name="Ссылка на видео")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
