from celery import shared_task



from materials.model import Course
from materials.services import send_mailing


@shared_task
def mailing_about_updates(course_id):
    """Функция отправления сообщений об обновлении курса клиентам"""
    course = Course.objects.get(pk=course_id)
    subscription_list = course.subscription.all()
    user_list = [subscription.user for subscription in subscription_list]
    subject = 'Обновление'
    body = f'Вышло обновление по курсу {course}'
    send_mailing(user_list, subject, body)


@shared_task
def send_message_about_like(user, lesson):
    """Функция отправки сообщения о лайке урока"""
    address = []
    subject = 'Урок понравился'
    body = f'Пользователь {user} поставил лайк уроку {lesson}'
    address.append(user)
    send_mailing(address, subject, body)