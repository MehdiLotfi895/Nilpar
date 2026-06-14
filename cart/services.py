# cart/services.py
from decimal import Decimal

from .cart import Cart as SessionCart
from main.models import OrderBasket


class DatabaseCart:
    """
    مدیریت سبد خرید در دیتابیس با استفاده از OrderBasket
    """

    def __init__(self, user):
        self.user = user

    def add(
        self,
        product,
        quantity=1,
        color=None,
        body_color=None,
        door_color=None,
        override=False
    ):
        quantity = int(quantity)

        max_allowed = getattr(product, 'max_number_order', 10) or 10
        stock = getattr(product, 'stock', 99) or 99

        basket_item, created = OrderBasket.objects.get_or_create(
            user=self.user,
            product=product,
            color=color,
            body_color=body_color,
            door_color=door_color,
            defaults={'number': 0}
        )

        if override:
            new_quantity = quantity
        else:
            new_quantity = basket_item.number + quantity

        if new_quantity > max_allowed:
            raise ValueError(f'حداکثر {max_allowed} عدد از این محصول قابل سفارش است')

        if new_quantity > stock:
            raise ValueError(f'فقط {stock} عدد از این محصول در انبار موجود است')

        if new_quantity <= 0:
            basket_item.delete()
            return 0

        basket_item.number = new_quantity
        basket_item.save()
        return new_quantity

    def remove(
        self,
        product,
        color=None,
        body_color=None,
        door_color=None
    ):
        OrderBasket.objects.filter(
            user=self.user,
            product=product,
            color=color,
            body_color=body_color,
            door_color=door_color
        ).delete()

    def update_quantity(
        self,
        product,
        quantity,
        color=None,
        body_color=None,
        door_color=None
    ):
        return self.add(
            product=product,
            quantity=quantity,
            color=color,
            body_color=body_color,
            door_color=door_color,
            override=True
        )

    def get_items(self):
        items = []

        basket_items = OrderBasket.objects.filter(
            user=self.user
        ).select_related(
            'product',
            'color',
            'body_color',
            'door_color'
        )

        for item in basket_items:
            old_price = Decimal(item.product.old_price)
            off_percent = Decimal(item.product.off)

            if off_percent > 0:
                discount_amount = (old_price * off_percent) / 100
                final_price = old_price - discount_amount
            else:
                final_price = old_price

            final_price = final_price.quantize(Decimal('0'))
            total = final_price * item.number

            items.append({
                'product': item.product,
                'color': item.color,
                'body_color': item.body_color,
                'door_color': item.door_color,
                'quantity': item.number,
                'old_price': int(old_price),
                'final_price': int(final_price),
                'total': int(total),
                'has_discount': off_percent > 0,
                'off_percent': int(off_percent),
            })

        return items

    def get_total_price(self):
        return sum(item['total'] for item in self.get_items())

    def get_total_items(self):
        return sum(item.number for item in OrderBasket.objects.filter(user=self.user))

    def clear(self):
        OrderBasket.objects.filter(user=self.user).delete()


class UnifiedCartService:
    """
    سرویس یکپارچه برای سبد خرید: دیتابیس برای کاربر لاگین و سشن برای مهمان
    """

    @staticmethod
    def get_cart(request):
        if request.user.is_authenticated:
            return DatabaseCart(request.user)
        return SessionCart(request)

    @staticmethod
    def merge_carts(request):
        if not request.user.is_authenticated:
            return

        session_cart = SessionCart(request)
        session_items = session_cart.get_items()

        if not session_items:
            return

        db_cart = DatabaseCart(request.user)

        for item in session_items:
            try:
                db_cart.add(
                    product=item['product'],
                    quantity=item['quantity'],
                    color=item.get('color'),
                    body_color=item.get('body_color'),
                    door_color=item.get('door_color'),
                )
            except ValueError:
                pass

        session_cart.clear()