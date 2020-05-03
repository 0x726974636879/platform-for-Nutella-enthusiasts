from math import ceil

import requests

from django.core.management.base import BaseCommand

from apps.openfoodfacts.constants import CATEGORIES_URL
from apps.openfoodfacts.models import Category, Product


class Command(BaseCommand):
    help = "Adding data to the database."
    category = None

    def insert_products(self, product_number, url):
        """
        Insert all products off each category into the database.
        Parameters
        ----------
        product_number : string
            Number of product.
        url : string
            Category url.

        Raises
        ------
            Exception : If there is any error during the product
            insertion.
        """
        total_page = ceil(product_number / 20)
        # Limit to 200 products per category.
        if total_page > 10:
            total_page = 11
        # Browse all pages of a category.
        products = list()
        for page in range(1, total_page):
            response = requests.get(f'{url}/{page}.json').json()
            # Add all products into a huge list.
            products += [
                Product(
                    product_name=p.get("product_name"),
                    code=p.get("code"),
                    img_url=p.get("url"),
                    salt=p["nutrient_levels"].get("salt"),
                    fat=p["nutrient_levels"].get("fat"),
                    sugars=p["nutrient_levels"].get("sugars"),
                    saturated_fat=p["nutrient_levels"].get("saturated-fat"),
                    warehouse=p.get("brands"),
                    allergens=p.get("allergens"),
                    nutrition_grades=p.get("nutrition_grades"),
                    category=self.category
                )
                for p in response["products"]
                if (p.get("product_name") and
                    p.get("nutrition_grades") and p.get("code"))
            ]
        self.stdout.write(f'ID #{self.category.id}.')
        self.stdout.write(f'{page} page(s) synchronisée(s).')
        self.stdout.write(f'{len(products)} produit(s) synchronisé(s).')
        # Insert all the products for a category into 'Product' table.
        try:
            Product.objects.bulk_create(products)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error during product insertion:\n{e}\n"
                )
            )

    def insert_category(self, category_name):
        """
        Insert a category into the database.
        Parameters
        ----------
        category_name : string
            category's name.

        Raises
        ------
            Exception : If there is any error during the category
            selection.
        """
        try:
            # Insert category into the database.
            self.category = Category.objects.create(name=category_name)
            self.category.save()
            self.stdout.write(
                self.style.HTTP_INFO(
                    f"Category {category_name} sync in progress.."
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error during category insertion:\n{e}\nexit\n"
                )
            )

    def truncate_tables(self):
        """
        Delete the data from each table.
        """
        try:
            tables = (Category, Product)
            # Drop the tables and reset the auto increment start number
            # to 1.
            for table in tables:
                table.objects.all().delete()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error during droping tables:\n{e}\nexit\n")
            )

    def handle(self, *args, **options):
        """
        Handle to add data to the database.
        """
        response = requests.get(CATEGORIES_URL).json()
        # Clean the database.
        self.truncate_tables()
        # Re-insert all categories and their products in the database.
        for category_number, category in enumerate(response['tags']):
            # Limit category number to 20.
            if category_number > 19:
                break
            self.insert_category(category['name'])
            self.insert_products(category['products'], category['url'])
            self.stdout.write(100 * '=')
        self.stdout.write(
            self.style.SUCCESS(
                "Synchronisation de la base de donnée effectuée avec success."
            )
        )
