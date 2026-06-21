from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "name_ar", "slug", "icon", "parent"]


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "sku", "name", "name_ar", "generic_name", "brand",
            "category", "category_name", "price", "stock", "image",
            "prescription_required", "in_stock", "dosage_form", "strength",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
