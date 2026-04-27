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
    
    
class Discount(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    percent_off = models.FloatField(verbose_name="Скидка в %")

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"


class Tax(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    percentage = models.FloatField(verbose_name="Налог в %")

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name="Товары")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Скидка")
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Налог")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id}"
    
    @property
    def get_currency(self):
        first_item = self.items.first()
        return first_item.currency if first_item else 'usd'
    
    @property
    def total_price(self):
        return sum(item.price for item in self.items.all())

    
