from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    """
    Category model.
    """
    name = models.CharField(max_length=400)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model.
    """
    product_name = models.CharField(max_length=200)
    code = models.CharField(max_length=30)
    img_url = models.CharField(max_length=400, blank=True, null=True)
    salt = models.CharField(max_length=10, blank=True, null=True)
    fat = models.CharField(max_length=10, blank=True, null=True)
    sugars = models.CharField(max_length=10, blank=True, null=True)
    saturated_fat = models.CharField(max_length=10, blank=True, null=True)
    warehouse = models.CharField(max_length=400, blank=True, null=True)
    allergens = models.CharField(max_length=400, blank=True, null=True)
    nutrition_grades = models.CharField(max_length=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class BackupProduct(models.Model):
    """
    History model.
    """
    product_code = models.CharField(max_length=30)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name
