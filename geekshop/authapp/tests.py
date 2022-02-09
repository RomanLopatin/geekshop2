from django.test import TestCase

# Create your tests here.
from authapp.models import ShopUser


class UserAuthTestCase(TestCase):
    username = 'django'
    password = 'geekbrains'
    email = 'django@gb.local'

    def setUp(self) -> None:
        self.superuser = ShopUser.objects.create_superuser(
            username=self.username,
            password=self.password,
            email=self.email
        )

    def test_login_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context['user'].is_anonymous)
        # данные пользователя
        self.client.login(username=self.username, password=self.password)
        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        # self.assertEqual(response.context['user'], self.username)

    def test_logout_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        # пробуем выйти
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)

        # с логином все должно быть хорошо
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('Ваша корзина, Пользователь', response.content.decode())

