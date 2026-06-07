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
            # اگر سبد خرید در سشن وجود نداشت، یک سبد خالی بساز
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    
    def _get_key(self, product_id, color_id):
        """
        ساخت کلید ترکیبی از product_id و color_id
        مثلاً: "5_3" یعنی محصول با id=5 و رنگ با id=3
        """
        return f"{product_id}_{color_id}"
    
    def _calculate_final_price(self, product):
        """
        محاسبه قیمت نهایی با احتساب تخفیف
        
        Returns:
            Decimal: قیمت نهایی بعد از تخفیف
        """
        old_price = Decimal(product.old_price)
        off_percent = Decimal(product.off)
        
        if off_percent > 0:
            discount_amount = (old_price * off_percent) / 100
            final_price = old_price - discount_amount
        else:
            final_price = old_price
        
        return final_price.quantize(Decimal('0'))  # حذف اعشار
    
    def _get_product_price_info(self, product):
        """
        دریافت اطلاعات قیمت محصول (قیمت اصلی و قیمت با تخفیف)
        
        Returns:
            dict: {'old_price': Decimal, 'final_price': Decimal, 'off_percent': int}
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
    
    def add(self, product, color, quantity=1, override=False):
        """
        اضافه کردن محصول با رنگ مشخص به سبد خرید
        
        Args:
            product: شیء محصول
            color: شیء رنگ
            quantity: تعداد مورد نظر برای اضافه کردن
            override: اگر True باشد، تعداد را جایگزین می‌کند نه جمع
        
        Returns:
            int: تعداد جدید در سبد خرید
        
        Raises:
            ValueError: اگر محدودیت‌ها نقض شود
        """
        key = self._get_key(product.id, color.id)
        
        # دریافت تعداد فعلی در سبد خرید (اگر وجود داشته باشد)
        current_quantity = self.cart[key]['quantity'] if key in self.cart else 0
        
        # محاسبه تعداد جدید
        if override:
            new_quantity = quantity
        else:
            new_quantity = current_quantity + quantity
        
        # اعتبارسنجی 1: حداکثر تعداد مجاز برای سفارش
        if new_quantity > product.max_number_order:
            raise ValueError(
                f'حداکثر تعداد قابل سفارش برای {product.name} '
                f'{product.max_number_order} عدد است.'
            )
        
        # اعتبارسنجی 2: موجودی انبار
        if new_quantity > product.stock:
            raise ValueError(
                f'موجودی {product.name} کافی نیست. '
                f'حداکثر {product.stock} عدد موجود است.'
            )
        
        # اگر تعداد صفر یا منفی شد، آیتم را حذف کن
        if new_quantity <= 0:
            if key in self.cart:
                del self.cart[key]
                self.save()
            return 0
        
        # دریافت اطلاعات قیمت
        price_info = self._get_product_price_info(product)
        
        # اگر آیتم وجود نداشت، ایجاد کن
        if key not in self.cart:
            self.cart[key] = {
                'product_id': product.id,
                'color_id': color.id,
                'quantity': 0,
                'old_price': str(price_info['old_price']),
                'final_price': str(price_info['final_price']),
                'off_percent': price_info['off_percent'],
                'has_discount': price_info['has_discount'],
                'color_name': color.color_name,
                'color_code': color.color_code,
                'product_name': product.name,
                'max_order_limit': product.max_number_order
            }
        
        # اضافه کردن تعداد
        self.cart[key]['quantity'] = new_quantity
        self.save()
        
        return new_quantity
    
    def remove(self, product, color):
        """
        حذف یک محصول با رنگ مشخص از سبد خرید
        """
        key = self._get_key(product.id, color.id)
        
        if key in self.cart:
            del self.cart[key]
            self.save()
    
    def update_quantity(self, product, color, quantity):
        """
        به‌روزرسانی تعداد محصول با رنگ مشخص
        
        Args:
            product: شیء محصول
            color: شیء رنگ
            quantity: تعداد جدید
        
        Raises:
            ValueError: اگر محدودیت‌ها نقض شود
        """
        key = self._get_key(product.id, color.id)
        
        if key not in self.cart:
            raise ValueError(f'{product.name} ({color.name}) در سبد خرید وجود ندارد.')
        
        # اعتبارسنجی
        if quantity > product.max_number_order:
            raise ValueError(
                f'حداکثر تعداد قابل سفارش برای {product.name} '
                f'{product.max_number_order} عدد است.'
            )
        
        if quantity > product.stock:
            raise ValueError(
                f'موجودی {product.name} کافی نیست. '
                f'حداکثر {product.stock} عدد موجود است.'
            )
        
        if quantity <= 0:
            # اگر تعداد صفر یا منفی شد، آیتم را حذف کن
            del self.cart[key]
        else:
            self.cart[key]['quantity'] = quantity
        
        self.save()
    
    def can_add(self, product, color, quantity=1):
        """
        بررسی کنید آیا می‌توان این تعداد را اضافه کرد یا نه
        بدون اینکه واقعاً اضافه کند
        
        Returns:
            tuple: (is_possible, message)
        """
        key = self._get_key(product.id, color.id)
        current_quantity = self.cart[key]['quantity'] if key in self.cart else 0
        new_quantity = current_quantity + quantity
        
        if new_quantity > product.max_number_order:
            return False, f"حداکثر {product.max_number_order} عدد قابل سفارش است"
        
        if new_quantity > product.stock:
            return False, f"فقط {product.stock} عدد موجود است"
        
        return True, "میتوانید اضافه کنید"
    
    def save(self):
        """
        ذخیره سبد خرید در سشن و علامت زدن تغییرات
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def get_items(self):
        """
        دریافت آیتم‌های سبد خرید با اطلاعات کامل از دیتابیس
        """
        items = []
        keys_to_remove = []
        
        for key, item in self.cart.items():
            try:
                # دریافت اطلاعات به‌روز از دیتابیس
                product = Product.objects.get(id=item['product_id'])
                color = ColorProduct.objects.get(id=item['color_id'])
                
                # دریافت اطلاعات قیمت به‌روز (قیمت و تخفیف ممکن است تغییر کرده باشد)
                price_info = self._get_product_price_info(product)
                final_price = price_info['final_price']
                old_price = price_info['old_price']
                
                # محاسبه جمع هر آیتم
                item_total = final_price * item['quantity']
                item_old_total = old_price * item['quantity']
                
                # محاسبه میزان تخفیف این آیتم
                discount_amount = item_old_total - item_total
                
                items.append({
                    'key': key,
                    'product': product,
                    'color': color,
                    'quantity': item['quantity'],
                    'old_price': old_price,
                    'final_price': final_price,
                    'item_old_total': item_old_total,
                    'item_total': item_total,
                    'discount_amount': discount_amount,
                    'has_discount': price_info['has_discount'],
                    'off_percent': price_info['off_percent'],
                    'color_name': color.color_name,
                    'color_code': color.color_code,
                    'product_name': product.name,
                })
            except (Product.DoesNotExist, ColorProduct.DoesNotExist):
                # اگر محصول یا رنگ حذف شده بود، آیتم را برای حذف علامت بزن
                keys_to_remove.append(key)
        
        # حذف آیتم‌های ناموجود
        for key in keys_to_remove:
            del self.cart[key]
        
        if keys_to_remove:
            self.save()
        
        return items
    
    def get_total_price(self):
        """
        جمع کل مبلغ سبد خرید (قیمت نهایی بعد از تخفیف)
        """
        total = Decimal('0')
        for item in self.cart.values():
            final_price = Decimal(item['final_price'])
            total += final_price * item['quantity']
        return total.quantize(Decimal('0'))
    
    def get_total_old_price(self):
        """
        جمع کل مبلغ سبد خرید قبل از تخفیف
        """
        total = Decimal('0')
        for item in self.cart.values():
            old_price = Decimal(item['old_price'])
            total += old_price * item['quantity']
        return total.quantize(Decimal('0'))
    
    def get_total_discount(self):
        """
        جمع کل تخفیف سبد خرید
        """
        return (self.get_total_old_price() - self.get_total_price()).quantize(Decimal('0'))
    
    def get_total_items(self):
        """
        تعداد کل محصولات در سبد خرید (تعداد، نه نوع)
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_items_count(self):
        """
        تعداد نوع محصولات در سبد خرید (تعداد آیتم‌های مجزا)
        """
        return len(self.cart)
    
    def clear(self):
        """
        خالی کردن کامل سبد خرید
        """
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
    
    def is_product_exists(self, product, color):
        """
        بررسی وجود محصول با رنگ مشخص در سبد خرید
        """
        key = self._get_key(product.id, color.id)
        return key in self.cart
    
    def get_item_quantity(self, product, color):
        """
        دریافت تعداد یک محصول با رنگ مشخص
        """
        key = self._get_key(product.id, color.id)
        if key in self.cart:
            return self.cart[key]['quantity']
        return 0
    
    def refresh_prices(self):
        """
        به‌روزرسانی قیمت‌ها در سبد خرید (در صورت تغییر قیمت یا تخفیف محصولات)
        """
        updated = False
        for key, item in self.cart.items():
            try:
                product = Product.objects.get(id=item['product_id'])
                price_info = self._get_product_price_info(product)
                
                # اگر قیمت یا تخفیف تغییر کرده بود، به‌روز کن
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
        
        Args:
            db_cart_items: لیست آیتم‌های سبد خرید از دیتابیس (مدل CartItem)
        """
        for db_item in db_cart_items:
            product = db_item.product
            color = db_item.color
            quantity = db_item.quantity
            
            try:
                # سعی کن به سبد خرید سشن اضافه کنی
                self.add(product, color, quantity, override=False)
            except ValueError:
                # اگر محدودیت وجود داشت، به همان مقداری که امکان دارد اضافه کن
                current_qty = self.get_item_quantity(product, color)
                max_allowed = min(product.max_number_order, product.stock)
                possible_qty = max_allowed - current_qty
                
                if possible_qty > 0:
                    try:
                        self.add(product, color, possible_qty, override=False)
                    except ValueError:
                        pass  # اگر نشد، نادیده بگیر
        
        self.save()