import smtplib
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


class StripeService:
    """Класс для сервиса Stripe"""
    def __init__(self, api_key):
        self.api_key = api_key

    # def create_payment(self, obj, user):
    #     stripe.api_key = self.api_key
    #     create_product = stripe.Product.create(name=obj.name)
    #
    #     price = stripe.Price.create(unit_amount=int(obj.price) * 100,
    #                                 currency='rub',
    #                                 product=create_product['id'])
    #
    #     session = stripe.checkout.Session.create(success_url='http://127.0.0.1:8000/',
    #                                              line_items=[{"price": price.id, "quantity": 1}],
    #                                              mode='payment', client_reference_id=user.id)
    #     return session
    #
    # def check_payment(self, session_id):
    #     stripe.api_key = self.api_key
    #
    #     session = stripe.checkout.Session.retrieve(session_id)
    #
    #     return session


def send_mailing(address, subject, body):
    """Функция отправки письма"""
    try:
        response = send_mail(
            subject=subject,
            message=body,
            from_email=EMAIL_HOST_USER,
            recipient_list=address,
            fail_silently=False,
        )
        return response
    except smtplib.SMTPException:
        raise smtplib.SMTPException