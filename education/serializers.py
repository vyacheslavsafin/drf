from rest_framework import serializers

from education.models import Course, Lesson, Payment, Subscription
from education.validators import VideoLinkValidator
from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title',)


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    validators = [VideoLinkValidator(field='video_link')]

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'course', 'video_link')


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title',)


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonListSerializer(many=True, read_only=True)
    course_subscription = serializers.SerializerMethodField()

    def get_course_subscription(self, obj):
        return Subscription.objects.filter(course=obj, user=self.context['request'].user).exists()

    def get_lessons_count(self, obj):
        return Lesson.objects.all().filter(course=obj).count()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('owner', 'course_subscription')


class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.SerializerMethodField()

    def get_payment_method(self, obj):
        if obj.payment_method == '1':
            return "Наличные"
        elif obj.payment_method == '2':
            return "Перевод на счет"

    class Meta:
        model = Payment
        fields = ('id', 'user', 'payment_date', 'course', 'payment_total', 'payment_method', 'session', 'is_successful')


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('course', 'payment_method')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    course = serializers.SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Subscription
        fields = ('id', 'user', 'course')
