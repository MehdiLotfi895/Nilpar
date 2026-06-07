# cart/signals.py
from django.contrib.auth.signals import user_logged_in ,user_login_failed
from django.dispatch import receiver
from .services import UnifiedCartService

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    """
    وقتی کاربر لاگین می‌کند، سبد خرید سشن با دیتابیس ادغام شود
    """
    if request:
        UnifiedCartService.merge_carts(request)

@receiver(user_login_failed)
def after_failed(**kwargs):
    print(1)