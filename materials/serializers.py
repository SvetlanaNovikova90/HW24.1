from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.model import Course, Lesson, Subscription
from materials.validators import YoutubeLinkValidator


class LessonSerializer(ModelSerializer):
    validators = [YoutubeLinkValidator(field="link_to_video")]

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons_list = LessonSerializer(source="lessons", many=True, read_only=True)

    @staticmethod
    def get_lessons_count(obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "lessons_count", "lessons_list")

    def get_is_subscribed(self, course):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=course
            ).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор Подписки"""

    class Meta:
        model = Subscription
        fields = "__all__"

    def to_representation(self, instance):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_staff or instance.user == user:
                return super().to_representation(instance)
            return {}
        return super().to_representation(instance)
