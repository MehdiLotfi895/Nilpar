# کدهای زیر را می‌توانید در یک فایل جدید به نام cart/views.py یا انتهای فایل main/views.py قرار دهید.
from django.shortcuts import  redirect, render,get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib import messages
from main.models import Product, ColorProduct, AddressInfo
from .services import UnifiedCartService

class CartDetailView(TemplateView):
    """نمایش صفحه سبد خرید"""
    template_name = 'orderbasket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_service = UnifiedCartService.get_cart(self.request)
        context['cart_items'] = cart_service.get_items()
        context['total_price'] = cart_service.get_total_price()
        context['total_items'] = cart_service.get_total_items()
        return context

class CartAddView(View):
    """افزودن محصول به سبد خرید"""
    def post(self, request, product_id):
        cart_service = UnifiedCartService.get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        
        color_name= request.POST.get('color')
        if not color_name:
            # اگر رنگ ارسال نشد، اولین رنگ محصول را انتخاب کن
            color = product.color.first()
        else:
            color = get_object_or_404(ColorProduct, color_name=color_name)
            
        quantity = request.POST.get('quantity', 1)
        
        try:
            cart_service.add(product=product, color=color, quantity=int(quantity))
            messages.success(request, f'محصول "{product.name}" با موفقیت به سبد خرید اضافه شد.')
        except ValueError as e:
            messages.error(request, str(e))
            
        return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))

class CartRemoveView(View):
    """حذف کامل محصول از سبد خرید"""
    def post(self, request, product_id, color_id):
        cart_service = UnifiedCartService.get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        color = get_object_or_404(ColorProduct, id=color_id)
        cart_service.remove(product, color)
        messages.success(request, 'محصول از سبد خرید حذف شد.')
        return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))

class CartUpdateQuantityView(View):
    """کاهش یا افزایش تعداد محصول با دکمه‌ها"""
    def post(self, request, product_id, color_id):
        cart_service = UnifiedCartService.get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        color = get_object_or_404(ColorProduct, id=color_id)
        action = request.POST.get('action') # 'increase' or 'decrease'
        # پیدا کردن تعداد فعلی محصول در سبد خرید
        current_qty = 0
        for item in cart_service.get_items():
            if item['product'].id == product.id and item['color'].id == color.id:
                current_qty = item['quantity']
                break
                
        try:
            if action == 'increase':
                cart_service.update_quantity(product, color, current_qty + 1)
            elif action == 'decrease':
                if current_qty > 1:
                    cart_service.update_quantity(product, color, current_qty - 1)
                else:
                    cart_service.remove(product, color)
        except ValueError as e:
            messages.error(request, str(e))
            
        return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))
    




