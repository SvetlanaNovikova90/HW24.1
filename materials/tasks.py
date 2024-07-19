from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.model import Course, Subscription
from materials.services import send_mailing


@shared_task
def mailing_about_updates(course_id):
    """Функция отправления сообщений об обновлении курса клиентам"""
    course = Course.objects.get(pk=course_id)
    subscription = Subscription.objects.get(course=course_id)
    # print("отправка")

    send_mail(
        subject="Обновление",
        message=f"Вышло обновление по курсу {course}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[subscription.user.email],
    )


@shared_task
def send_message_about_like(user, lesson):
    """Функция отправки сообщения о лайке урока"""
    address = []
    subject = "Урок понравился"
    body = f"Пользователь {user} поставил лайк уроку {lesson}"
    address.append(user)
    send_mailing(address, subject, body)
