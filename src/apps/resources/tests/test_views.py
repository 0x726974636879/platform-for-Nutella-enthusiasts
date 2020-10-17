from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.resources.models import BackupProduct, Product
from .constants import CREDENTIALS
from .utils import create_products


class ShowProductViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create X product to a category.
        """
        create_products(5)

    def test_view_url_exists_and_can_watch_a_product(self):
        product_id = Product.objects.order_by('?').first().id
        response = self.client.get(f"/products/{product_id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        product_id = Product.objects.order_by('?').first().id
        response = self.client.get(
            reverse("resources:products_list", args=[product_id])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        product_id = Product.objects.order_by('?').first().id
        response = self.client.get(
            reverse("resources:products_list", args=[product_id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/product_details.html")

    def test_product_nonexistent(self):
        product_id = 123456789
        self.assertRaises(
            Product.DoesNotExist, self.client.get, f"/products/{product_id}/"
        )


class SearchProductViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create X product to a category.
        """
        create_products(10)

    def test_view_url_exists(self):
        response = self.client.get("/products/search/")
        self.assertNotEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("resources:products_search"))
        self.assertNotEqual(response.status_code, 404)

    def test_redirect_home_if_no_product_found(self):
        response = self.client.get(
            reverse("resources:products_search") + "?word=no_product"
        )
        self.assertEqual(response.status_code, 301)

    def test_redirect_product_list_if_product_found(self):
        response = self.client.get(
            "{}?word={}".format(
                reverse('resources:products_search'),
                Product.objects.order_by('?').first().product_name
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/products"))


class ShowProductViewViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create X product to a category.
        """
        create_products(10)

    def test_view_url_exists(self):
        product_id = Product.objects.order_by('?').first().id
        response = self.client.get(f"/products/{product_id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        product_id = Product.objects.order_by('?').first().id
        response = self.client.get(
            reverse("resources:products_list", args=[product_id])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        product_id = Product.objects.order_by('?').first().id
        response = self.client.get(
            reverse("resources:products_list", args=[product_id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/product_details.html")


class SavedProductsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create X product to a category.
        """
        # Create products.
        create_products(10)
        # Create user.
        test_user1 = User.objects.create_user(**CREDENTIALS)
        test_user1.save()
        # Create product saved by the user.
        for product in Product.objects.all()[:5]:
            BackupProduct.objects.create(
                product_code=product.code,
                category_name=product.category.name,
                user=test_user1
            )

    def test_view_url_exists(self):
        _ = self.client.login(**CREDENTIALS)
        response = self.client.get("/products/saved/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        _ = self.client.login(**CREDENTIALS)
        response = self.client.get(reverse("resources:products_saved"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        _ = self.client.login(**CREDENTIALS)
        response = self.client.get(reverse("resources:products_saved"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/products_saved.html")

    def test_redirect_if_not_logged(self):
        response = self.client.get(reverse("resources:products_saved"))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_product_saved(self):
        _ = self.client.login(**CREDENTIALS)
        user = User.objects.all().first()
        response = self.client.get(reverse("resources:products_saved"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["object_list"]),
            len(BackupProduct.objects.filter(user=user))
        )


class SaveProductViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create X product to a category.
        """
        # Create products.
        create_products(10)
        # Create user.
        test_user1 = User.objects.create_user(**CREDENTIALS)
        test_user1.save()

    def test_save_product_with_url(self):
        product_id = Product.objects.order_by('?').first().id
        self.client.login(**CREDENTIALS)
        self.client.post(
            "/products/save/",
            {"product_id": product_id}
        )
        self.assertEqual(
            BackupProduct.objects.filter(
                user=User.objects.get(username=CREDENTIALS["username"])
            ).count(),
            1
        )

    def test_save_product_by_url_name(self):
        product_id = Product.objects.order_by('?').first().id
        self.client.login(**CREDENTIALS)
        self.client.post(
            reverse("resources:products_save"),
            {"product_id": product_id}
        )
        self.assertEqual(
            BackupProduct.objects.filter(
                user=User.objects.get(username=CREDENTIALS["username"])
            ).count(),
            1
        )

    def test_cannot_save_without_loggin(self):
        product_id = Product.objects.order_by('?').first().id
        self.client.post(
            "/products/save/", {"product_id": product_id}
        )
        self.assertNotEqual(
            BackupProduct.objects.filter(
                user=User.objects.get(username=CREDENTIALS["username"])
            ).count(),
            1
        )
