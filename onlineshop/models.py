from django.db import models

# Create your models here.


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    category_name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.category_name


class Product(TimeStampModel):
    product_name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Order(TimeStampModel):
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.pk}"
