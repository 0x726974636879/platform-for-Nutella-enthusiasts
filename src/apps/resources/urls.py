from django.urls import path
from . import views

app_name = "resources"

urlpatterns = [
    path(
        "products/<int:pk>/",
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
    ),
    path(
        "products/save/",
        views.SaveProductView.as_view(),
        name="products_save"
    )
]
