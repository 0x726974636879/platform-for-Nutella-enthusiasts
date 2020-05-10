from django.urls import path
from . import views

app_name = "openfoodfacts"

urlpatterns = [
    path(
        "products/<int:pk>",
        views.ShowProductView.as_view(),
        name="products_list"
    ),
    path(
        "products/search/",
        views.SearchProductView.as_view(),
        name="products_search"
    ),
    path(
        "products/saved/",
        views.SavedProductsListView.as_view(),
        name="products_saved"
    )
]
