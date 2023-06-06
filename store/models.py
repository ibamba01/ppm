from django.contrib.auth.models import User

from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

class Product(models.Model):
    user = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.TextField(blank=True)
    price = models.IntegerField() #è il moodo piu comune con cui si rappresentano i prezzi in un database
    image = models.ImageField(upload_to="uploads/product_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created_at',) #ordina i prodotti in ordine di creazione


    def __str__(self):
        return self.title

    def get_display_price(self):
        return self.price / 100


class Order(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    address = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    paid_amount = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    merchant_id = models.CharField(max_length=64,)

    created_by = models.ForeignKey(User, related_name="orders", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    def get_display_price(self):
        return self.price / 100