from django.contrib import auth
from django.contrib.auth import get_user_model, get_user
from django.test import TestCase, Client
from django.urls import reverse

from apps.product.models import Category
from apps.vendor.forms import ProductForm
from apps.vendor.models import Vendor


class BaseTest(TestCase):
    def setUp(self):
        self.add_product_url = reverse('add_product')
        self.login_url = reverse('login')
        self.vendor_admin_url = reverse('vendor_admin')
        self.upgrade_vendor_url = reverse('upgrade_vendor')
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="user0", email="testemail@gmail.com",
                                                         password="xyzas1029",
                                                         is_vendor=True)
        self.user_without_is_vendor = get_user_model().objects.create_user(username="user1", email="testemail@gmail.it",
                                                                           password="xyzas1029",
                                                                           is_vendor=False)
        Vendor.objects.get_or_create(created_by=self.user)
        Category.objects.get_or_create(title="test_category", slug="test_category")

        return super().setUp()

    def tearDown(self):
        self.user.delete()
        self.user_without_is_vendor.delete()
        return super().tearDown()


class TestAddProduct(BaseTest):
    def test_add_product_view_deny_anonymous_get(self):
        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + "?next=" + self.add_product_url)

    def test_add_product_view_deny_anonymous_post(self):
        response = self.client.post(self.add_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + "?next=" + self.add_product_url)

    def test_add_product_view_without_vendor_get(self):
        self.client.force_login(get_user_model().objects.filter(username="user1").first())
        user = get_user(self.client)
        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.upgrade_vendor_url + "?next=" + self.add_product_url)

    def test_add_product_view_without_vendor_post(self):
        self.client.force_login(get_user_model().objects.filter(username="user1").first())
        user = auth.get_user(self.client)

        response = self.client.post(self.add_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.upgrade_vendor_url + "?next=" + self.add_product_url)

    def test_add_product_view_with_vendor_get_success(self):
        self.client.force_login(get_user_model().objects.filter(username="user0").first())
        user = auth.get_user(self.client)

        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendor/add_product.html')

    def test_add_product_view_with_vendor_post_blank_data(self):
        self.client.force_login(get_user_model().objects.filter(username="user0").first())
        user = auth.get_user(self.client)

        response = self.client.post(self.add_product_url, {})
        self.assertFormError(response, 'form', 'category', 'This field is required.')
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'price', 'This field is required.')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendor/add_product.html')

    def test_add_product_view_with_vendor_post_invalid_category(self):
        self.client.force_login(get_user_model().objects.filter(username="user0").first())
        user = auth.get_user(self.client)
        product = {'category': 0, 'title': 'test', 'price': 10}
        response = self.client.post(self.add_product_url, product)
        self.assertFormError(response, 'form', 'category',
                             'Select a valid choice. That choice is not one of the available choices.')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendor/add_product.html')

    def test_add_product_view_with_vendor_post_valid_form(self):
        self.client.force_login(get_user_model().objects.filter(username="user0").first())
        user = auth.get_user(self.client)

        product = {'category': 1, 'title': 'test', 'price': 10, 'quantity': 1, }
        form = ProductForm(product)

        self.assertTrue(form.is_valid())
        response = self.client.post(self.add_product_url, product)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("vendor_admin"))
