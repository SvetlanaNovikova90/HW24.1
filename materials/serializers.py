from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.model import Course, Lesson, Subscription
from materials.validators import YoutubeLinkValidator


class LessonSerializer(ModelSerializer):
    validators = [YoutubeLinkValidator(field='link_to_video')]

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons_list = LessonSerializer(source="lessons", many=True, read_only=True)

    @staticmethod
    def get_lessons_count(obj):
        return Lesson.objects.filter(
            course=obj
        ).count()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "lessons_count", "lessons_list")


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор Подписки """

    class Meta:
        model = Subscription
        fields = "__all__"
