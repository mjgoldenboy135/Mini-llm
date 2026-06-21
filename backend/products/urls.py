from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("", ProductListView.as_view(), name="product_list"),
    path("<uuid:id>/", ProductDetailView.as_view(), name="product_detail"),
]
