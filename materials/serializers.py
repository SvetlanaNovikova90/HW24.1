from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.model import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    number_of_lessons = SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set", many=True, read_only=True)

    def get_number_of_lessons(self, course):
        return Lesson.objects.filter(pk=course.pk).count()

    class Meta:
        model = Course
        fields = "__all__"
