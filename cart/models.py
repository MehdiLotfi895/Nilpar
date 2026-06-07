# cart/models.py
from django.db import models
from django.conf import settings
from main.models import Product, ColorProduct

class CartItem(models.Model):
    """
    مدل سبد خرید برای کاربران احراز هویت شده
    """
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
    color = models.ForeignKey(
        ColorProduct, 
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # هر کاربر فقط یک بار می‌تونه یک محصول با یک رنگ خاص رو داشته باشه
        unique_together = ['user', 'product', 'color']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.color.name}) x{self.quantity}"
