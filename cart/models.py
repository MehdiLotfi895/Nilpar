# cart/models.py
from django.db import models
from django.conf import settings
from main.models import Product, ColorProduct

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    # محصولات تک رنگ
    color = models.ForeignKey(
        ColorProduct,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items_single'
    )

    # محصولات دو رنگ
    body_color = models.ForeignKey(
        ColorProduct,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cartitems_body'
    )

    door_color = models.ForeignKey(
        ColorProduct,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cartitems_door'
    )

    quantity = models.PositiveSmallIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            'user',
            'product',
            'color',
            'body_color',
            'door_color',
        )

    def __str__(self):
        return f'{self.product}'
