import random
import string

from apps.resources.models import Category, Product


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
