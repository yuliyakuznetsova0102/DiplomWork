from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.models import User, UserRoles
from django.core import mail
from django.test import override_settings


class UserTests(APITestCase):
    "Cоздает тестовые данные"
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '+1234567890',
            'password': 'testpass123',
            'password2': 'testpass123'
        }

    def test_user_registration(self):
        "Проверяет регистрацию нового пользователя"
        url = reverse('register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_login(self):
        "Проверяет аутентификацию пользователя (получение JWT-токенов)"
        User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_password_reset(self):
        "Тестирует процесс сброса пароля (отправка email)"
        User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

        with override_settings(FRONTEND_URL='http://test.local'):
            with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
                response = self.client.post(
                    reverse('reset_password'),
                    {'email': 'test@example.com'},
                    format='json'
                )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_confirm(self):
        "Проверяет подтверждение сброса пароля"
        user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='oldpass123'
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = reverse('reset_password_confirm')
        data = {
            'uid': uid,
            'token': token,
            'new_password': 'newpass123',
            'new_password2': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password('newpass123'))

    def test_admin_creation(self):
        "Проверяет создание пользователя с ролью администратора"
        admin = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpass123',
            role='admin'
        )
        self.assertEqual(admin.role, UserRoles.ADMIN)
        self.assertTrue(admin.is_admin)
