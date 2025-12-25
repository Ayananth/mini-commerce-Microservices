from django.db import models


class Order(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
