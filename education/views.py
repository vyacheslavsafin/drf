from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from education.models import Lesson, Course, Payment, Subscription
from education.paginators import Paginator
from education.serializers import LessonSerializer, CourseDetailSerializer, PaymentSerializer, PaymentCreateSerializer, \
    SubscriptionSerializer, SubscriptionListSerializer
from education.permissions import IsNotStaff, IsOwnerOrStaff


class CourseViewSet(ModelViewSet):
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    pagination_class = Paginator

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Course.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Course.objects.all()
        else:
            return False

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            return False
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff:
            return False
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = Paginator

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Lesson.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Lesson.objects.all()
        else:
            return False


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsNotStaff]


    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsNotStaff]


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'payment_method')
    ordering_fields = ('payment_date',)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsNotStaff]

    def create(self, request, *args, **kwargs):
        for subscription in Subscription.objects.filter(user=self.request.user):
            if subscription.course.id == request.data.get('course'):
                raise PermissionDenied('Вы уже подписаны на этот курс')
        return super().create(request, *args, **kwargs)


class SubscriptionListAPIView(ListAPIView):
    serializer_class = SubscriptionListSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionDestroyAPIView(DestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsNotStaff]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
