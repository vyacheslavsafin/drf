from celery import shared_task
from django.core.mail import send_mail

from config import settings
from education.models import Subscription


@shared_task
def update_course_mailing(course_id):
    for subscription in Subscription.objects.filter(course_id=course_id):
        send_mail(
            subject='Обновление курса',
            message=f'Курс {subscription.course} обновлен.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
        )
