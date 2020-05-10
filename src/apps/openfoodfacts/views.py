from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Product


class SearchProductView(TemplateView):
    """
    Product page view.
    """
    template_name = "openfoodfacts/product_details.html"

    def get(self, request, **kwargs):
        """
        Override GET method to make a request to find the product.
        """
        word = request.GET.get("word")
        substitutes = None
        # Get a product that starts with the given word if no product
        # has been found take a product whose name contains the given
        # word.
        product = Product.objects.filter(
            Q(product_name__startswith=word) | Q(product_name__contains=word)
        ).order_by("product_name").first()
        if product:
            # Get a list of better products than the one chosen.
            substitutes = Product.get_substitutes(product.category.id)
            context = {"product": product, "substitutes": substitutes}
            return render(request, self.template_name, context)
        return render(request, self.template_name, {"no_products": True})
