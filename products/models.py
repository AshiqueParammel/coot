
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from categories.models import category

class Color(models.Model):
    color_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=15)

    def __str__(self):
        return self.color_name


class Size(models.Model):
    size_range = models.CharField(max_length=60)

    def __str__(self):
        return self.size_range


class Product(models.Model):
    product_name = models.CharField(unique=True, max_length=50)
    product_price = models.IntegerField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True)
    product_description = models.TextField(max_length=50,default="")

    def __str__(self):
        return self.product_name






class ProductReview(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    review_text = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
