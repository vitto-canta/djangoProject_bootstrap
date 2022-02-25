from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import RegistrationForm


class CustomUserTest(TestCase):

    def test_create_user_valid(self):
        start_time = timezone.now()
        user = get_user_model().objects.create_user(
            username="JohnLennon", password="secretpassword", name="John",
            surname="Lennon", email="john.lennon@gmeil.com"
        )
        end_time = timezone.now()
        self.assertEqual(user.email, 'john.lennon@gmeil.com')
        self.assertEqual(user.username, "JohnLennon")
        self.assertEqual(user.name, "John")
        self.assertEqual(user.surname, "Lennon")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_vendor)
        self.assertFalse(user.is_costumer)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(end_time > user.created > start_time)
        self.assertTrue(end_time > user.last_login > start_time)
        self.assertTrue(user.check_password("secretpassword"))
        expected_representation_account = "JohnLennon"
        self.assertEqual(expected_representation_account, str(user))

    def test_create_user_without_username(self):
        with self.assertRaises(ValueError, msg='You must provide a username'):
            user = get_user_model().objects.create_user(
                password="secretpassword", name="John",
                surname="Lennon", email="john.lennon@gmeil.com"
            )

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError, msg='You must provide an email address'):
            user = get_user_model().objects.create_user(
                username="JohnLennon",
                password="secretpassword", name="John",
                surname="Lennon",
            )

    def test_create_user_without_password(self):
        user = get_user_model().objects.create_user(
            username="JohnLennon",
            email="john.lennon@gmeil.com",
            name="John",
            surname="Lennon",
        )
        self.assertTrue(user.password is not None)

    def test_create_superuser_valid(self):
        start_time = timezone.now()
        user = get_user_model().objects.create_superuser(
            username="RingoStarr", password="secretpassword",
            email="ringo.starr@gmeil.com",
        )
        end_time = timezone.now()
        self.assertEqual(user.email, 'ringo.starr@gmeil.com')
        self.assertEqual(user.username, "RingoStarr")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_vendor)
        self.assertTrue(user.is_costumer)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(end_time > user.created > start_time)
        self.assertTrue(end_time > user.last_login > start_time)
        self.assertTrue(user.check_password("secretpassword"))
        expected_representation_account = "RingoStarr"
        self.assertEqual(expected_representation_account, str(user))

    def test_create_superuser_is_vendor_false(self):
        with self.assertRaises(ValueError, msg='Superuser must be assigned to is_vendor=True. '):
            user = get_user_model().objects.create_superuser(
                username="RingoStarr", password="secretpassword",
                email="ringo.starr@gmeil.com", is_vendor=False
            )

    def test_create_superuser_is_costumer_false(self):
        with self.assertRaises(ValueError, msg='Superuser must be assigned to is_costumer=True. '):
            user = get_user_model().objects.create_superuser(
                username="RingoStarr", password="secretpassword",
                email="ringo.starr@gmeil.com", is_costumer=False
            )

    def test_create_superuser_is_superuser_false(self):
        with self.assertRaises(ValueError, msg='Superuser must be assigned to is_superuser=True. '):
            user = get_user_model().objects.create_superuser(
                username="RingoStarr", password="secretpassword",
                email="ringo.starr@gmeil.com", is_superuser=False
            )


class BaseRegisterTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'xyzas1029',
            'password2': 'xyzas1029',
            'name': 'fullname',
            'is_vendor': '1',
            'is_costumer': '1',
        }

        self.user_same_username = {
            'email': 'mail@gmail.com',
            'username': 'username',
            'password': 'xyzas1029',
            'password2': 'xyzas1029',
            'name': 'fullname',
            'is_vendor': '0',
            'is_costumer': '0',
        }

        self.user_same_email = {
            'email': 'testemail@gmail.com',
            'username': 'same_email',
            'password': 'xyzas1029',
            'password2': 'xyzas1029',
            'name': 'fullname',
            'is_vendor': '0',
            'is_costumer': '0',
        }

        self.user_short_password = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'tes',
            'password2': 'tes',
            'name': 'fullname',
            'is_vendor': '0',
            'is_costumer': '0',
        }
        self.user_unmatching_password = {

            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'teslatt',
            'password2': 'teslatto',
            'name': 'fullname',
            'is_vendor': '0',
            'is_costumer': '0',
        }

        self.user_invalid_email = {

            'email': 'test.com',
            'username': 'username',
            'password': 'teslatt',
            'password2': 'teslatt',
            'name': 'fullname',
            'is_vendor': '0',
            'is_costumer': '0',
        }

        self.user_without_email = {
            'username': 'username',
            'password': 'xyzas1029',
            'password2': 'xyzas1029',
            'name': 'fullname',
            'is_vendor': '0',
            'is_costumer': '0',
        }

        self.user_without_username = {
            'email': 'testemail@gmail.com',
            'password': 'xyzas1029',
            'password2': 'xyzas1029',
            'name': 'fullname',
            'is_vendor': '0',
            'is_costumer': '0',
        }

        self.user_without_is_vendor = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'xyzas1029',
            'password2': 'xyzas1029',
            'name': 'fullname',
            'is_costumer': '0',
        }

        self.user_without_is_costumer = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'xyzas1029',
            'password2': 'xyzas1029',
            'name': 'fullname',
            'is_vendor': '0',
        }

        self.user_without_password = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password2': 'xyzas1029',
            'name': 'fullname',
            'is_vendor': '0',
            'is_costumer': '0',
        }

        self.user_without_password2 = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'xyzas1029',
            'name': 'fullname',
            'is_vendor': '0',
            'is_costumer': '0',
        }

        return super().setUp()


class RegisterTest(BaseRegisterTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_can_register_user(self):
        form = RegistrationForm(self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_password2(), self.user['password2'])

        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("frontpage"))

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

        my_user = get_user_model().objects.get(username=self.user["username"])
        self.assertTrue(my_user.has_perms(
            ["account.search_item", "account.view_item", "account.view_rate", "account.be_notified",
             "account.sell_item", "account.confirm_shipment", "account.get_paid", "account.view_vendor_admin",
             "account.read_review", "account.buy_item", "account.view_costumer_admin", "account.confirm_delivery",
             "account.write_review", "account.save_item"]))

    def test_cant_register_user_withshortpassword(self):
        form = RegistrationForm(self.user_short_password)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.register_url, self.user_short_password, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_user_with_invalid_email(self):
        form = RegistrationForm(self.user_invalid_email)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.register_url, self.user_invalid_email, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_user_with_unmatching_passwords(self):
        form = RegistrationForm(self.user_unmatching_password)
        self.assertFalse(form.is_valid())
        form.has_error('password2', code="pw_not_match")

        response = self.client.post(self.register_url, self.user_unmatching_password, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_user_with_taken_email(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.register_url, self.user_same_email, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    def test_cant_register_user_with_taken_username(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.register_url, self.user_same_username, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    def test_cant_register_user_without_email(self):
        form = RegistrationForm(self.user_without_email)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.register_url, self.user_without_email, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_user_without_username(self):
        form = RegistrationForm(self.user_without_username)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.register_url, self.user_without_username, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_user_without_is_vendor(self):
        form = RegistrationForm(self.user_without_is_vendor)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.register_url, self.user_without_is_vendor, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_user_without_is_costumer(self):
        form = RegistrationForm(self.user_without_is_costumer)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.register_url, self.user_without_is_costumer, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_user_without_password(self):
        form = RegistrationForm(self.user_without_password)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.register_url, self.user_without_password, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_user_without_password2(self):
        form = RegistrationForm(self.user_without_password2)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.register_url, self.user_without_password2, format='text/html')
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)
