from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib import messages

from main.models import Product, ColorProduct
from .services import UnifiedCartService


def _to_int(value, default=1):
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return default


def _get_optional_color(color_id):
    if not color_id:
        return None
    return get_object_or_404(ColorProduct, id=color_id)


def _extract_variant_data(request):
    """
    از فرم، همه‌ی حالت‌ها را می‌خواند:
    - color / product_color / color_id  -> رنگ تک‌گانه
    - body_color                       -> رنگ بدنه
    - door_color                       -> رنگ درب
    """
    return {
        "color_id": request.POST.get("color") or request.POST.get("product_color") or request.POST.get("color_id"),
        "body_color_id": request.POST.get("body_color") or request.POST.get("body_color_id"),
        "door_color_id": request.POST.get("door_color") or request.POST.get("door_color_id"),
    }


class CartDetailView(TemplateView):
    """نمایش صفحه سبد خرید"""
    template_name = "orderbasket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_service = UnifiedCartService.get_cart(self.request)
        context["cart_items"] = cart_service.get_items()
        context["total_price"] = cart_service.get_total_price()
        context["total_items"] = cart_service.get_total_items()
        context["current_page"] = "orderbasket"
        return context


class CartAddView(View):
    """
    افزودن محصول اصلی + افزودن اکسسوری‌های انتخاب‌شده
    اکسسوری‌ها با همان تعداد محصول اصلی، جداگانه به سبد اضافه می‌شوند.
    """
    def post(self, request, product_id):
        cart_service = UnifiedCartService.get_cart(request)
        product = get_object_or_404(Product, id=product_id)

        quantity = _to_int(request.POST.get("quantity", 1))
        variant_data = _extract_variant_data(request)

        # رنگ تک‌گانه
        color = _get_optional_color(variant_data["color_id"])

        # رنگ بدنه / درب
        body_color = _get_optional_color(variant_data["body_color_id"])
        door_color = _get_optional_color(variant_data["door_color_id"])

        # اگر هیچ رنگی نفرستاده شد، برای محصول تک‌رنگ اولین رنگ را بردار
        if color is None and body_color is None and door_color is None:
            if product.color.exists():
                color = product.color.first()

        # اگر محصول دو رنگ است و چیزی نفرستاده‌ای، مقدار پیش‌فرض از خود محصول
        if body_color is None and color is None and product.body_color.exists():
            body_color = product.body_color.first()

        if door_color is None and color is None and product.door_color.exists():
            door_color = product.door_color.first()

        accessory_ids = request.POST.getlist("accessories")
        accessory_ids = [int(x) for x in accessory_ids if str(x).isdigit()]

        try:
            # محصول اصلی
            cart_service.add(
                product=product,
                quantity=quantity,
                color=color,
                body_color=body_color,
                door_color=door_color,
            )

            # اکسسوری‌ها: هر کدام به‌صورت آیتم جدا و با همان تعداد
            if accessory_ids:
                accessory_products = product.accessories.filter(id__in=accessory_ids).distinct()
                for accessory in accessory_products:
                    cart_service.add(
                        product=accessory,
                        quantity=quantity,
                        color=accessory.color.first(),
                    )

            messages.success(
                request,
                f'محصول "{product.name}" با موفقیت به سبد خرید اضافه شد.'
            )

        except ValueError as e:
            messages.error(request, str(e))

        return redirect(request.META.get("HTTP_REFERER", "cart:cart_detail"))


class CartRemoveView(View):
    """حذف کامل یک آیتم از سبد"""
    def post(self, request, product_id):
        cart_service = UnifiedCartService.get_cart(request)
        product = get_object_or_404(Product, id=product_id)

        variant_data = _extract_variant_data(request)

        color = _get_optional_color(variant_data["color_id"])
        body_color = _get_optional_color(variant_data["body_color_id"])
        door_color = _get_optional_color(variant_data["door_color_id"])

        cart_service.remove(
            product=product,
            color=color,
            body_color=body_color,
            door_color=door_color,
        )

        messages.success(request, "محصول از سبد خرید حذف شد.")
        return redirect(request.META.get("HTTP_REFERER", "cart:cart_detail"))


class CartUpdateQuantityView(View):
    """افزایش/کاهش تعداد آیتم"""
    def post(self, request, product_id):
        cart_service = UnifiedCartService.get_cart(request)
        product = get_object_or_404(Product, id=product_id)

        action = request.POST.get("action")  # increase / decrease
        variant_data = _extract_variant_data(request)

        color = _get_optional_color(variant_data["color_id"])
        body_color = _get_optional_color(variant_data["body_color_id"])
        door_color = _get_optional_color(variant_data["door_color_id"])

        current_qty = 0
        for item in cart_service.get_items():
            same_product = item["product"].id == product.id

            same_color = (
                (item.get("color") and color and item["color"].id == color.id) or
                (item.get("color") is None and color is None)
            )

            same_body = (
                (item.get("body_color") and body_color and item["body_color"].id == body_color.id) or
                (item.get("body_color") is None and body_color is None)
            )

            same_door = (
                (item.get("door_color") and door_color and item["door_color"].id == door_color.id) or
                (item.get("door_color") is None and door_color is None)
            )

            if same_product and same_color and same_body and same_door:
                current_qty = item["quantity"]
                break

        try:
            if action == "increase":
                cart_service.update_quantity(
                    product=product,
                    quantity=current_qty + 1,
                    color=color,
                    body_color=body_color,
                    door_color=door_color,
                )
            elif action == "decrease":
                if current_qty > 1:
                    cart_service.update_quantity(
                        product=product,
                        quantity=current_qty - 1,
                        color=color,
                        body_color=body_color,
                        door_color=door_color,
                    )
                else:
                    cart_service.remove(
                        product=product,
                        color=color,
                        body_color=body_color,
                        door_color=door_color,
                    )
        except ValueError as e:
            messages.error(request, str(e))

        return redirect(request.META.get("HTTP_REFERER", "cart:cart_detail"))