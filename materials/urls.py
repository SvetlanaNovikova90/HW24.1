from django.urls import path
from rest_framework.routers import SimpleRouter


from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonDestroyApiView,
    LessonUpdateApiView,
    LessonListApiView,
    LessonRetrieveApiView,
    LessonCreateApiView,
    SubscriptionAPIView,
)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)
# router.register("subscription", SubscriptionViewSet, basename="subscription")

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("lesson/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path(
        "lesson/<int:pk>/destroy/",
        LessonDestroyApiView.as_view(),
        name="lesson_destroy",
    ),
    path(
        "lesson/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"
    ),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
]
urlpatterns += router.urls
