import requests


from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import (
    DetailView, ListView, View
)

from .constants import PRODUCTS_URL
from .models import Product, BackupProduct


class SearchProductView(View):
    """
    Product page view.
    """
    def get(self, request, **kwargs):
        """
        Override GET method to make a request to find the product.
        """
        word = request.GET.get("word")
        # Get a product that starts with the given word if no product
        # has been found take a product whose name contains the given
        # word.
        product = Product.objects.filter(
            Q(product_name__startswith=word) | Q(product_name__contains=word)
        ).order_by("product_name").first()
        if product:
            return redirect("openfoodfacts:products_list", pk=product.id)
        return redirect("openfoodfacts:products_list", no_products=True)


class ShowProductView(DetailView):
    model = Product
    template_name = "openfoodfacts/product_details.html"

    def get(self, request, **kwargs):
        """
        Override GET method to make a request to find some substitutes.
        """
        # Get a list of better products than the one shown.
        substitutes = self.model.get_substitutes(kwargs.get("pk"))
        context = {
            "product": Product.objects.get(pk=kwargs.get("pk")),
            "substitutes": substitutes
        }
        return render(request, self.template_name, context)


class SavedProductsListView(ListView):
    """
    Saved products page view.
    """
    template_name = "openfoodfacts/products_saved.html"

    def get_queryset(self):
        """
        Override get_queryset method to show all the product saved by
        the current user.
        to show the real product from the product
        code, if the product is in the database show it directly
        otherwise make an API call to retrieve the product, otherwise
        do not show it in the list of saved products.
        """
        current_user = self.request.user
        queryset = BackupProduct.objects.filter(user=current_user)
        object_list = []
        for p in queryset:
            try:
                product = Product.objects.get(code=p.product_code)
                object_list.append({
                    "id": product.id,
                    "product_name": product["product_name"],
                    "code": p.product_code,
                    "img_url": product["image_url"],
                    "url": product["url"],
                    "salt": product["salt"],
                    "fat": product["fat"],
                    "sugars": product["sugars"],
                    "saturated_fat": product["saturated-fat"],
                    "warehouse": product["brands"],
                    "allergens": product["allergens"],
                    "nutrition_grades": product["nutrition_grades"]
                })
            except Exception:
                response = requests.get(f"{PRODUCTS_URL}{p.product_code}.json")
                if response.status_code == 200:
                    r_json = response.json()["product"]
                    object_list.append({
                        "id": "NID",
                        "product_name": r_json.get("product_name"),
                        "code": p.product_code,
                        "img_url": r_json.get("image_url"),
                        "url": r_json.get("url"),
                        "salt": r_json["nutrient_levels"].get("salt"),
                        "fat": r_json["nutrient_levels"].get("fat"),
                        "sugars": r_json["nutrient_levels"].get("sugars"),
                        "saturated_fat": r_json["nutrient_levels"].get("saturated-fat"),
                        "warehouse": r_json.get("brands"),
                        "allergens": r_json.get("allergens"),
                        "nutrition_grades": r_json.get("nutrition_grades")
                    })

        return object_list


class SaveProductView(View):
    """
    Save a product page view.
    """
    def post(self, request, *args, **kwargs):
        """
        Override post method to save a product to our favorites.
        """
        current_user = self.request.user
        product = Product.objects.get(pk=self.request.POST.get("product_id"))
        bp = BackupProduct.objects.create(
            product_code=product.code, user=current_user
        )
        bp.save()
        return redirect("openfoodfacts:products_list", pk=product.id)
