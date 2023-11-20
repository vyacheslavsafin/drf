from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from education.models import Course, Lesson, Subscription
from users.models import User


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test course')
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test description',
            course=self.course,
            owner=self.user,
        )

    def test_lesson_list(self):
        """ Тестирование списка уроков """
        response = self.client.get(reverse('lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'count': 1,
                          'next': None,
                          'previous': None,
                          'results': [
                              {'id': self.lesson.id,
                               'title': self.lesson.title,
                               'description': self.lesson.description,
                               'course': self.lesson.course.title,
                               'video_link': self.lesson.video_link,
                               }
                          ]
                          }
                         )

    def test_lesson_retrieve(self):
        """ Тестирование просмотра урока """
        response = self.client.get(reverse('lesson-retrieve', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': self.lesson.id,
                          'title': self.lesson.title,
                          'description': self.lesson.description,
                          'course': self.lesson.course.title,
                          'video_link': self.lesson.video_link,
                          }
                         )

    def test_lesson_create(self):
        """ Тестирование создания урока """
        data = {
            'title': 'Test lesson 2',
            'description': 'Test description 2',
            'course': self.course,
            'video_link': 'https://www.youtube.com'
        }
        response = self.client.post(reverse('lesson-create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_link_validation(self):
        """ Тестирование валидации ссылки на видео """
        data = {
            'title': 'Test lesson 3',
            'description': 'Test description 3',
            'course': self.course,
            'video_link': 'https://www.rutube.com',
        }
        response = self.client.post(reverse('lesson-create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Ссылка должна содержать youtube.com']})

    def test_lesson_update(self):
        """ Тестирование обновления урока """
        data = {
            'title': 'Test change',
            'description': 'Test description change',
            'course': self.course,
        }
        response = self.client.put(reverse('lesson-update', args=[self.lesson.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': self.lesson.id,
                          'title': data['title'],
                          'description': data['description'],
                          'course': self.lesson.course.title,
                          'video_link': self.lesson.video_link,
                          }
                         )

    def test_lesson_delete(self):
        """ Тестирование удаления урока """
        response = self.client.delete(reverse('lesson-delete', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test course')
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test description',
            course=self.course,
            owner=self.user,
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

    def test_subscription_list(self):
        """ Тестирование списка подписок """
        response = self.client.get(reverse('subscription-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [
                             {'id': self.subscription.id,
                              'user': self.subscription.user.email,
                              'course': self.subscription.course.title,
                              }
                         ])

    def test_subscription_delete(self):
        """ Проверка удаления подписки """
        response = self.client.delete(reverse('subscription-delete', args=[self.subscription.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)