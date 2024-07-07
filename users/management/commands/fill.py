import json

from django.core.management import BaseCommand

from materials.model import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):

    @staticmethod
    def json_read_payments():
        with open('data.json', encoding="UTF-16") as file:
            data = json.load(file)
        return [item for item in data if item['model'] == 'users.payments']

    def handle(self, *args, **options):
        Payments.objects.all().delete()

        payments_for_create = []
        for payment in Command.json_read_payments():
            payments_for_create.append(
                Payments(id=payment['pk'],
                         user=User.objects.get(pk=payment["fields"]["user"]),
                         date_of_payment=payment['fields']['date_of_payment'],
                         paid_course=Course.objects.get(pk=payment['fields']['paid_course']),
                         paid_lesson=Lesson.objects.get(pk=payment['fields']['paid_lesson']),
                         payment_amount=payment['fields']['payment_amount'],
                         payment_method=payment['fields']['payment_method'])
            )
        Payments.objects.bulk_create(payments_for_create)
