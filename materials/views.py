from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status

from django.utils import timezone
from drf_yasg import openapi
from rest_framework.decorators import action

from materials.tasks import mailing_about_updates
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
    CreateAPIView,
)
from rest_framework.views import APIView

from materials.model import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.permissions import IsModerator, IsOwner
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="description from swagger_auto_schema via method_decorator"
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    """Course view set"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    def get_permissions(
        self,
    ):  # Проверка прав группы модераторов для курсов (нельзя создавать и удалять курс).
        if self.action in ("create",):
            self.permission_classes = [~IsModerator]
        elif self.action in ("update",):
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [~IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        mailing_about_updates.delay(course.pk)


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsOwner, IsModerator]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsOwner, IsModerator]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsOwner, ~IsModerator]


class LessonCreateApiView(CreateAPIView):
    """Создание урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]


post_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["course_id"],
    properties={
        "course_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID of the course"
        )
    },
)

post_response_schema = openapi.Response(
    description="Subscription status message",
    examples={"application/json": {"message": "Подписка добавлена"}},
)

# Схема для метода GET
get_response_schema = openapi.Response(
    description="List of subscriptions", schema=SubscriptionSerializer(many=True)
)


class SubscriptionAPIView(APIView):
    @action(detail=True, authods=("post",))
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        # get_or_create возвращает кортеж из двух элементов:
        # объект и bool(создан или получен из базы)
        subs_item, created = Subscription.objects.get_or_create(
            user=user, course=course_item
        )

        if created:
            message = "подписка добавлена"
        else:
            subs_item.delete()
            message = "подписка удалена"

        return Response(message)
