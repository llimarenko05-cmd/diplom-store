from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StockReceipt, Sale


@receiver(post_save, sender=StockReceipt)
def increase_product_quantity(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.quantity += instance.quantity
        product.save()


@receiver(post_save, sender=Sale)
def decrease_product_quantity(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        if product.quantity >= instance.quantity:
            product.quantity -= instance.quantity
            product.save()