# cart/context_processors.py
from .services import UnifiedCartService

def cart(request):
    """
    Context processor برای دسترسی به اطلاعات کلی سبد خرید در تمامی صفحات و قالب‌ها
    """
    if request.path.startswith('/admin/'):
        return {}
        
    cart_service = UnifiedCartService.get_cart(request)
    
    return {
        'cart': cart_service,
        'user_order_basket': {
            'total_number': cart_service.get_total_items(),
            'total_price': int(cart_service.get_total_price()),
        }
    }