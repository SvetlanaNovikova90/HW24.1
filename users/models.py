from django.db import models

from django.contrib.auth.models import AbstractUser

from materials.model import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    avatar = models.ImageField(
        upload_to="users/avatars", **NULLABLE, verbose_name="Аватар"
    )
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="Телефон")
    country = models.CharField(max_length=35, **NULLABLE, verbose_name="Страна")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payments(models.Model):
    user = models.ForeignKey(
        User,
        **NULLABLE,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
    )
    date_of_payment = models.DateField(auto_now_add=True, verbose_name="дата оплаты")

    paid_course = models.ForeignKey(
        Course,
        **NULLABLE,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        **NULLABLE,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный урок",
    )
    payment_amount = models.IntegerField(verbose_name="сумма оплаты")
    payment_method = models.CharField(
        max_length=50,
        verbose_name="Способ оплаты",
        choices=[("cash", "Cash"), ("non-cash", "Non-cash")],
    )
