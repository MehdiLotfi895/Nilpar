# cart/cart.py
from decimal import Decimal
from django.conf import settings
from main.models import Product, ColorProduct


class Cart:
    def __init__(self, request):
        """
        مقداردهی اولیه سبد خرید از سشن جاری
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def _get_key(self, product_id, color_id=None, body_color_id=None, door_color_id=None):
        """
        ساخت کلید ترکیبی یکتا بر اساس نوع رنگ‌ها:
        - تک‌رنگ: f"{product_id}_c{color_id}"
        - دو رنگ: f"{product_id}_b{body_color_id}_d{door_color_id}"
        - بدون رنگ: f"{product_id}_none"
        """
        if body_color_id is not None and door_color_id is not None:
            return f"{product_id}_b{body_color_id}_d{door_color_id}"
        elif color_id is not None:
            return f"{product_id}_c{color_id}"
        else:
            return f"{product_id}_none"

    def _calculate_final_price(self, product):
        """
        محاسبه قیمت نهایی با احتساب تخفیف
        """
        old_price = Decimal(product.old_price)
        off_percent = Decimal(product.off)

        if off_percent > 0:
            discount_amount = (old_price * off_percent) / 100
            final_price = old_price - discount_amount
        else:
            final_price = old_price

        return final_price.quantize(Decimal('0'))

    def _get_product_price_info(self, product):
        """
        دریافت اطلاعات قیمت محصول (قیمت اصلی و قیمت با تخفیف)
        """
        old_price = Decimal(product.old_price)
        off_percent = product.off
        final_price = self._calculate_final_price(product)

        return {
            'old_price': old_price,
            'final_price': final_price,
            'off_percent': off_percent,
            'has_discount': off_percent > 0
        }

    def add(self, product, quantity=1, color=None, body_color=None, door_color=None, override=False):
        """
        اضافه کردن محصول با رنگ‌های مشخص به سبد خرید
        (پشتیبانی از تک‌رنگ، دو رنگ و بدون رنگ)
        """
        quantity = int(quantity)

        # تعریف شناسه‌های رنگ
        color_id = color.id if color else None
        body_color_id = body_color.id if body_color else None
        door_color_id = door_color.id if door_color else None

        key = self._get_key(product.id, color_id, body_color_id, door_color_id)

        current_quantity = self.cart[key]['quantity'] if key in self.cart else 0
        new_quantity = quantity if override else current_quantity + quantity

        # اعتبارسنجی
        if new_quantity > product.max_number_order:
            raise ValueError(
                f'حداکثر تعداد قابل سفارش برای {product.name} '
                f'{product.max_number_order} عدد است.'
            )
        if new_quantity > product.stock:
            raise ValueError(
                f'موجودی {product.name} کافی نیست. '
                f'حداکثر {product.stock} عدد موجود است.'
            )

        if new_quantity <= 0:
            if key in self.cart:
                del self.cart[key]
                self.save()
            return 0

        price_info = self._get_product_price_info(product)

        if key not in self.cart:
            self.cart[key] = {
                'product_id': product.id,
                'quantity': 0,
                'old_price': str(price_info['old_price']),
                'final_price': str(price_info['final_price']),
                'off_percent': price_info['off_percent'],
                'has_discount': price_info['has_discount'],
                'product_name': product.name,
                'max_order_limit': product.max_number_order,
                # ذخیره رنگ‌ها برای استفاده در get_items
                'color_id': color_id,
                'body_color_id': body_color_id,
                'door_color_id': door_color_id,
            }

        self.cart[key]['quantity'] = new_quantity
        self.save()
        return new_quantity

    def remove(self, product, color=None, body_color=None, door_color=None):
        """
        حذف یک محصول با رنگ‌های مشخص از سبد خرید
        """
        color_id = color.id if color else None
        body_color_id = body_color.id if body_color else None
        door_color_id = door_color.id if door_color else None
        key = self._get_key(product.id, color_id, body_color_id, door_color_id)

        if key in self.cart:
            del self.cart[key]
            self.save()

    def update_quantity(self, product, quantity, color=None, body_color=None, door_color=None):
        """
        به‌روزرسانی تعداد محصول با رنگ‌های مشخص
        """
        self.add(product, quantity, color, body_color, door_color, override=True)

    def can_add(self, product, quantity=1, color=None, body_color=None, door_color=None):
        """
        بررسی امکان اضافه کردن تعداد مشخص از محصول با رنگ‌های داده شده
        (بدون تغییر واقعی سبد)
        """
        color_id = color.id if color else None
        body_color_id = body_color.id if body_color else None
        door_color_id = door_color.id if door_color else None
        key = self._get_key(product.id, color_id, body_color_id, door_color_id)

        current_quantity = self.cart[key]['quantity'] if key in self.cart else 0
        new_quantity = current_quantity + quantity

        if new_quantity > product.max_number_order:
            return False, f"حداکثر {product.max_number_order} عدد قابل سفارش است"
        if new_quantity > product.stock:
            return False, f"فقط {product.stock} عدد موجود است"
        return True, "میتوانید اضافه کنید"

    def save(self):
        """ذخیره سبد خرید در سشن"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_items(self):
        """دریافت آیتم‌های سبد خرید با اطلاعات کامل از دیتابیس"""
        items = []
        keys_to_remove = []

        for key, item in self.cart.items():
            try:
                product = Product.objects.get(id=item['product_id'])

                # دریافت اشیاء رنگ بر اساس IDهای ذخیره شده
                color = None
                body_color = None
                door_color = None

                if item.get('color_id'):
                    color = ColorProduct.objects.get(id=item['color_id'])
                if item.get('body_color_id'):
                    body_color = ColorProduct.objects.get(id=item['body_color_id'])
                if item.get('door_color_id'):
                    door_color = ColorProduct.objects.get(id=item['door_color_id'])

                price_info = self._get_product_price_info(product)
                final_price = price_info['final_price']
                old_price = price_info['old_price']

                item_total = final_price * item['quantity']
                item_old_total = old_price * item['quantity']
                discount_amount = item_old_total - item_total

                items.append({
                    'key': key,
                    'product': product,
                    'color': color,
                    'body_color': body_color,
                    'door_color': door_color,
                    'quantity': item['quantity'],
                    'old_price': old_price,
                    'final_price': final_price,
                    'item_old_total': item_old_total,
                    'item_total': item_total,
                    'discount_amount': discount_amount,
                    'has_discount': price_info['has_discount'],
                    'off_percent': price_info['off_percent'],
                    'product_name': product.name,
                })
            except (Product.DoesNotExist, ColorProduct.DoesNotExist):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.cart[key]
        if keys_to_remove:
            self.save()

        return items

    def get_total_price(self):
        """جمع کل مبلغ سبد خرید (قیمت نهایی بعد از تخفیف)"""
        total = Decimal('0')
        for item in self.cart.values():
            total += Decimal(item['final_price']) * item['quantity']
        return total.quantize(Decimal('0'))

    def get_total_old_price(self):
        """جمع کل مبلغ سبد خرید قبل از تخفیف"""
        total = Decimal('0')
        for item in self.cart.values():
            total += Decimal(item['old_price']) * item['quantity']
        return total.quantize(Decimal('0'))

    def get_total_discount(self):
        """جمع کل تخفیف سبد خرید"""
        return (self.get_total_old_price() - self.get_total_price()).quantize(Decimal('0'))

    def get_total_items(self):
        """تعداد کل محصولات در سبد خرید (تعداد، نه نوع)"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_items_count(self):
        """تعداد نوع محصولات در سبد خرید (تعداد آیتم‌های مجزا)"""
        return len(self.cart)

    def clear(self):
        """خالی کردن کامل سبد خرید"""
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def is_product_exists(self, product, color=None, body_color=None, door_color=None):
        """بررسی وجود محصول با رنگ‌های مشخص در سبد خرید"""
        color_id = color.id if color else None
        body_color_id = body_color.id if body_color else None
        door_color_id = door_color.id if door_color else None
        key = self._get_key(product.id, color_id, body_color_id, door_color_id)
        return key in self.cart

    def get_item_quantity(self, product, color=None, body_color=None, door_color=None):
        """دریافت تعداد یک محصول با رنگ‌های مشخص"""
        color_id = color.id if color else None
        body_color_id = body_color.id if body_color else None
        door_color_id = door_color.id if door_color else None
        key = self._get_key(product.id, color_id, body_color_id, door_color_id)
        if key in self.cart:
            return self.cart[key]['quantity']
        return 0

    def refresh_prices(self):
        """به‌روزرسانی قیمت‌ها در سبد خرید (در صورت تغییر قیمت یا تخفیف محصولات)"""
        updated = False
        for key, item in self.cart.items():
            try:
                product = Product.objects.get(id=item['product_id'])
                price_info = self._get_product_price_info(product)

                if (str(price_info['final_price']) != item['final_price'] or
                    str(price_info['old_price']) != item['old_price']):
                    item['old_price'] = str(price_info['old_price'])
                    item['final_price'] = str(price_info['final_price'])
                    item['off_percent'] = price_info['off_percent']
                    item['has_discount'] = price_info['has_discount']
                    updated = True
            except Product.DoesNotExist:
                pass

        if updated:
            self.save()

    def merge_with_db_cart(self, db_cart_items):
        """
        ادغام سبد خرید سشن با سبد خرید دیتابیس (برای وقتی کاربر لاگین می‌کند)
        db_cart_items: لیست آیتم‌های مدل CartItem (با فیلدهای color, body_color, door_color)
        """
        for db_item in db_cart_items:
            product = db_item.product
            quantity = db_item.number
            color = db_item.color
            body_color = db_item.body_color
            door_color = db_item.door_color

            try:
                self.add(
                    product=product,
                    quantity=quantity,
                    color=color,
                    body_color=body_color,
                    door_color=door_color,
                    override=False
                )
            except ValueError:
                # اگر محدودیت وجود داشت، به همان مقداری که امکان دارد اضافه کن
                current_qty = self.get_item_quantity(product, color, body_color, door_color)
                max_allowed = min(product.max_number_order, product.stock)
                possible_qty = max_allowed - current_qty
                if possible_qty > 0:
                    try:
                        self.add(
                            product=product,
                            quantity=possible_qty,
                            color=color,
                            body_color=body_color,
                            door_color=door_color,
                            override=False
                        )
                    except ValueError:
                        pass  # اگر نشد، نادیده بگیر
        self.save()