from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Название продукта", max_length=100)
    quantity = models.PositiveIntegerField("Количество")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"


