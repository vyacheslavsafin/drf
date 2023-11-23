import stripe
from django.core.mail import send_mail
from celery import shared_task
from config import settings
from education.models import Subscription, Payment


@shared_task
def update_course_mailing(course_id):
    for subscription in Subscription.objects.filter(course_id=course_id):
        send_mail(
            subject='Обновление курса',
            message=f'Курс {subscription.course} обновлен.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
        )


def get_session(serializer: Payment):
    """ Получает сессию для оплаты курса """
    course_title = serializer.course.title
    product = stripe.Product.create(name=course_title)
    price = stripe.Price.create(
        unit_amount=serializer.course.price * 100,
        currency='rub',
        product=product.id,
    )
    session = stripe.checkout.Session.create(
        success_url='https://example.com/success',
        line_items=[
            {
                'price': price.id,
                'quantity': 1,
            }
        ],
        mode='payment',
        customer_email=serializer.user.email
    )
    send_payment_link_to_mail(session.url, serializer.user.email)
    return session


def retrieve_session(session):
    """ Получаем детали сессии"""
    return stripe.checkout.Session.retrieve(session)


def send_payment_link_to_mail(url, email):
    send_mail(
        subject='Оплата курса',
        message=f'Ссылка для оплаты курса: {url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
