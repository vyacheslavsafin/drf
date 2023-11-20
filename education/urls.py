from django.urls import path
from rest_framework import routers

from education.views import LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, CourseViewSet, PaymentListAPIView, PaymentCreateAPIView, SubscriptionCreateAPIView, \
    SubscriptionListAPIView, SubscriptionDestroyAPIView

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),

    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>/delete/', SubscriptionDestroyAPIView.as_view(), name='subscription-delete'),
] + router.urls
