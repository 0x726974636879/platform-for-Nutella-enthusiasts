import random
import string

from django.contrib.auth.models import User
from django.test import TestCase

from apps.resources.models import Category, BackupProduct, Product


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


def fill_database(nb_product):
    """
    """
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
                nutrition_grades=random.choice(
                    ('a', 'b', 'c', 'd', 'e')
                ),
                category=category
            )
        )
    Product.objects.bulk_create(products)


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="category_a")

    def test_name_label(self):
        category = Category.objects.order_by('?').first()
        field_label = category._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_name_max_length(self):
        category = Category.objects.order_by('?').first()
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 400)

    def test_object_name_is_name(self):
        category = Category.objects.order_by('?').first()
        self.assertEquals(f"{category.name}", str(category))


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create X product to a category.
        """
        fill_database(1000)

    def test_product_name_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("product_name").verbose_name
        self.assertEquals(field_label, "product name")

    def test_code_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("code").verbose_name
        self.assertEquals(field_label, "code")

    def test_img_url_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("img_url").verbose_name
        self.assertEquals(field_label, "img url")

    def test_url_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("url").verbose_name
        self.assertEquals(field_label, "url")

    def test_salt_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("salt").verbose_name
        self.assertEquals(field_label, "salt")

    def test_fat_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("fat").verbose_name
        self.assertEquals(field_label, "fat")

    def test_sugars_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("sugars").verbose_name
        self.assertEquals(field_label, "sugars")

    def test_saturated_fat_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("saturated_fat").verbose_name
        self.assertEquals(field_label, "saturated fat")

    def test_warehouse_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("warehouse").verbose_name
        self.assertEquals(field_label, "warehouse")

    def test_allergens_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("allergens").verbose_name
        self.assertEquals(field_label, "allergens")

    def test_nutrition_grades_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("nutrition_grades").verbose_name
        self.assertEquals(field_label, "nutrition grades")

    def test_category_label(self):
        product = Product.objects.order_by('?').first()
        field_label = product._meta.get_field("category").verbose_name
        self.assertEquals(field_label, "category")

    def test_product_name_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("product_name").max_length
        self.assertEquals(max_length, 400)

    def test_code_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("code").max_length
        self.assertEquals(max_length, 30)

    def test_img_url_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("img_url").max_length
        self.assertEquals(max_length, 400)

    def test_url_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("url").max_length
        self.assertEquals(max_length, 400)

    def test_salt_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("salt").max_length
        self.assertEquals(max_length, 10)

    def test_fat_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("fat").max_length
        self.assertEquals(max_length, 10)

    def test_sugars_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("sugars").max_length
        self.assertEquals(max_length, 10)

    def test_saturated_fat_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("saturated_fat").max_length
        self.assertEquals(max_length, 10)

    def test_warehouse_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("warehouse").max_length
        self.assertEquals(max_length, 400)

    def test_allergens_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("allergens").max_length
        self.assertEquals(max_length, 400)

    def test_nutrition_grades_max_length(self):
        product = Product.objects.order_by('?').first()
        max_length = product._meta.get_field("nutrition_grades").max_length
        self.assertEquals(max_length, 1)

    def test_object_name_is_product_name(self):
        product = Product.objects.order_by('?').first()
        self.assertEqual(f"{product.product_name}", str(product))

    def test_substitute_list_length(self):
        product = Product.objects.filter(nutrition_grades='d').first()
        substitutes = Product.get_substitutes(product.id)
        self.assertEquals(substitutes.count(), 12)

    def test_substitute_order(self):
        product = Product.objects.filter(nutrition_grades='e').first()
        substitutes = list(Product.get_substitutes(product.id))
        self.assertEqual(
            list(Product.objects.order_by("nutrition_grades")[:12]),
            substitutes
        )


class BackupProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fill_database(1000)
        credentials = {
            "username": "testuser1",
            "email": "testuser1@free.fr",
            "password": "1X<ISRUkw+tuK"
        }
        BackupProduct.objects.create(
            product_code=Product.objects.order_by('?').first().code,
            category_name=Product.objects.order_by('?').first().category.name,
            user=User.objects.create_user(**credentials)
        )

    def test_product_code_label(self):
        backup_product = BackupProduct.objects.order_by('?').first()
        field_label = \
            backup_product._meta.get_field("product_code").verbose_name
        self.assertEquals(field_label, "product code")

    def test_category_name_label(self):
        backup_product = BackupProduct.objects.order_by('?').first()
        field_label = \
            backup_product._meta.get_field("category_name").verbose_name
        self.assertEquals(field_label, "category name")

    def test_user_label(self):
        backup_product = BackupProduct.objects.order_by('?').first()
        field_label = backup_product._meta.get_field("user").verbose_name
        self.assertEquals(field_label, "user")

    def test_product_code_max_length(self):
        backup_product = BackupProduct.objects.order_by('?').first()
        max_length = backup_product._meta.get_field("product_code").max_length
        self.assertEquals(max_length, 30)

    def test_category_name_max_length(self):
        backup_product = BackupProduct.objects.order_by('?').first()
        max_length = backup_product._meta.get_field("category_name").max_length
        self.assertEquals(max_length, 400)

    def test_object_name_is_product_code(self):
        backup_product = BackupProduct.objects.order_by('?').first()
        self.assertEqual(f"{backup_product.product_code}", str(backup_product))
