from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentsListApiView, PaymentsCreateApiView, UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path("payment/", PaymentsListApiView.as_view(), name='payment_list'),
    path("payment/create/", PaymentsCreateApiView.as_view(), name='payment_create'),
]
urlpatterns += router.urls
