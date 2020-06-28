import random
import string

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.resources.models import Category, BackupProduct, Product


credentials = {
    "username": "testuser1",
    "email": "testuser1@free.fr",
    "password": "1X<ISRUkw+tuK"
}


def random_string(string_length=8):
    """
    Generate a random string with a predefine length.

    Parameters
    ----------
    string_length : int
        Length of the sequence.
        If no length given a sequence of 8 characters will be
        generate.

    Returns
    -------
        : str
        Random sequence of characters.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def create_products(nb_product):
    """
    Create x products with x categories.

    Parameters
    ----------
    nb_product : int
        Number of products you wish to create
    """
    grades = ('a', 'b', 'c', 'd', 'e')
    category = Category.objects.create(name="category_a")
    products = []
    for _ in range(nb_product):
        products.append(
            Product(
                product_name=f"product_{random_string()}",
                code=random_string(20),
                img_url=random_string(100),
                url=random_string(100),
                salt=random_string(),
                fat=random_string(),
                sugars=random_string(),
                saturated_fat=random_string(),
                warehouse=random_string(100),
                allergens=random_string(100),
                nutrition_grades=random.choice(grades),
                category=category
            )
        )
    Product.objects.bulk_create(products)


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
        response = self.client.get("/products/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("resources:products_list", args=['1'])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("resources:products_list", args=['1'])
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
        test_user1 = User.objects.create_user(**credentials)
        test_user1.save()
        # Create product saved by the user.
        for product in Product.objects.all()[:5]:
            BackupProduct.objects.create(
                product_code=product.code,
                category_name=product.category.name,
                user=test_user1
            )

    def test_view_url_exists(self):
        _ = self.client.login(**credentials)
        response = self.client.get("/products/saved/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        _ = self.client.login(**credentials)
        response = self.client.get(reverse("resources:products_saved"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        _ = self.client.login(**credentials)
        response = self.client.get(reverse("resources:products_saved"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/products_saved.html")

    def test_redirect_if_not_logged(self):
        response = self.client.get(reverse("resources:products_saved"))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_product_saved(self):
        _ = self.client.login(**credentials)
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
        test_user1 = User.objects.create_user(**credentials)
        test_user1.save()

    def test_save_product_with_url(self):
        product_id = Product.objects.order_by('?').first().id
        self.client.login(**credentials)
        self.client.post(
            "/products/save/",
            {"product_id": product_id}
        )
        self.assertEqual(
            BackupProduct.objects.filter(
                user=User.objects.get(username=credentials["username"])
            ).count(),
            1
        )

    def test_save_product_by_url_name(self):
        product_id = Product.objects.order_by('?').first().id
        self.client.login(**credentials)
        self.client.post(
            reverse("resources:products_save"),
            {"product_id": product_id}
        )
        self.assertEqual(
            BackupProduct.objects.filter(
                user=User.objects.get(username=credentials["username"])
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
                user=User.objects.get(username=credentials["username"])
            ).count(),
            1
        )
