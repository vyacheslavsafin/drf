from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса', **NULLABLE)
    preview = models.ImageField(upload_to='education/', verbose_name='Превью курса', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    price = models.PositiveIntegerField(default=1000, verbose_name='Стоимость курса')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока', **NULLABLE)
    preview = models.ImageField(upload_to='education/', verbose_name='Превью урока', **NULLABLE)
    video_link = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payments', **NULLABLE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс')
    payment_total = models.PositiveIntegerField(verbose_name='Сумма оплаты', **NULLABLE)
    payment_method = models.CharField(choices=[('1', 'Наличные'), ('2', 'Перевод на счет')], verbose_name='Способ оплаты')
    is_successful = models.BooleanField(default=False, verbose_name='Статус платежа')
    session = models.CharField(max_length=150, verbose_name='Сессия для оплаты', **NULLABLE)

    def __str__(self):
        return f"{self.payment_date}:{self.user} - {self.course}"

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ('-payment_date',)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_subscriptions')

    def __str__(self):
        return f"{self.user}({self.course})"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        