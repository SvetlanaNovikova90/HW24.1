import datetime

import pytz
from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_login():
    """Функция проверки пользователя по дате входа"""
    users = User.objects.filter(is_active=True)
    if users.exists():
        for user in users:
            if datetime.now(
                pytz.timezone("Europe/Moscow")
            ) - user.last_login > datetime.timedelta(weeks=4):
                user.is_active = False
                user.save()
