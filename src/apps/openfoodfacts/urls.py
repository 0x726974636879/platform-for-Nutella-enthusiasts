from django.urls import path
from . import views

app_name = "openfoodfacts"

urlpatterns = [
    path(
        "search_product/",
        views.SearchProductView.as_view(),
        name="search_product"
    ),
]
