import uuid
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to="categories/", null=True, blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children"
    )

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, blank=True)
    generic_name = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    prescription_required = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    dosage_form = models.CharField(max_length=100, blank=True)
    strength = models.CharField(max_length=100, blank=True)
    storage_conditions = models.CharField(max_length=255, blank=True)
    side_effects = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["barcode"]),
            models.Index(fields=["prescription_required"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def in_stock(self):
        return self.stock > 0
