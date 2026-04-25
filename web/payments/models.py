from django.db import models


class Item(models.Model):
    CURRENCY_CHOICES = (
        ('usd', 'USD'),
        ('eur', 'EUR'),
    )

    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.PositiveIntegerField(verbose_name="Цена")
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='usd',
        verbose_name="Валюта"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency.upper()}"

    
