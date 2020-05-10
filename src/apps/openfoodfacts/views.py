from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, TemplateView, View

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
        """
        current_user = self.request.user
        return BackupProduct.objects.filter(user=current_user)
