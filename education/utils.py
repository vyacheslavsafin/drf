from django.core.mail import send_mail
from config import settings
from education.models import Subscription


def update_course_mailing(serializer):
    for subscription in Subscription.objects.filter(course_id=serializer.instance.id):
        send_mail(
            subject='Обновление курса',
            message=f'Курс {serializer.instance.id} обновлен.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
        )