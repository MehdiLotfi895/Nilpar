# views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView,TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout
from django.utils import timezone
from django.db.models import Q ,F ,Sum,DecimalField, Value,Prefetch
from .models import Product, Order, HandOverOrder, AddressInfo, CustomUser, OTP ,Question ,Comment,Header_top,CategoryMain,SliderImage,Blog,OrderBasket,ColorProduct,OrderItem,AdItem,AdSection,DeliverySettings,LatestProducts, BestSellersProuducts
from .forms import PhoneForm, OTPForm, RegisterForm,AddAddressForm,ProfileForm,AddressUpdateForm
from django.db.models.functions import Coalesce
from django.db.models.expressions import ExpressionWrapper, CombinedExpression
from django.db import models
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.core.mail import send_mail
import requests
from django.views import View
from django.http import HttpResponse
from django.conf import settings
import jdatetime

# ========== صفحه اصلی ==========
class Home(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'home.html'       

    def get_queryset(self):
        return Product.objects.only('name','old_price','off','slug','id').annotate(
            price= F('old_price')*(100-F('off'))/100
        ).prefetch_related('images','color').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_image']=SliderImage.objects.all().select_related('category_main').order_by('created')
        context['comments']=Comment.objects.filter(state='c').select_related('product','user').prefetch_related('product__images').order_by('-created_at')
        context['blogs']=Blog.objects.all().order_by('-created')[:4]
        from django.db.models import Prefetch

        aditem_prefetch = Prefetch(
            'image',
            queryset=AdItem.objects.select_related('product')
        )
        
        context['ad_section_first'] = (
            AdSection.objects
            .exclude(state='repose', title='')
            .select_related('category_main')
            .prefetch_related(aditem_prefetch)
            .first()
        )
        
        context['ad_section_second'] = (
            AdSection.objects
            .filter(state='active', title__isnull=True)
            .select_related('category_main')
            .prefetch_related(aditem_prefetch)
            .first()
        )
        context['current_page']="home"
        context['lastest_products']=LatestProducts.objects.first().products.only('name','old_price','off','slug','id').annotate(
            price= F('old_price')*(100-F('off'))/100
        ).prefetch_related('images','color').order_by('-created_at').all()
        context['best_sellers_products']=BestSellersProuducts.objects.first().products.only('name','old_price','off','slug','id').annotate(
            price= F('old_price')*(100-F('off'))/100
        ).prefetch_related('images','color').order_by('-created_at').all()
        
        # ========== سبد خرید حذف شد - به جای آن از cart app استفاده کن ==========
        # if self.request.user.is_authenticated:
        #     context['user_order_basket']=OrderBasket.objects.filter(user=self.request.user).select_related('product','color').prefetch_related('product__images').annotate(price=F('product__old_price')*(100-F('product__off'))/100).aggregate(total_price=Sum(F('number') * F('price')),total_number=Sum(F('number')))   

        return context
    
    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == "search_box":
            search_query = request.POST.get('search_input', '').strip()
            if search_query:
                return redirect('products',search_query)
            else:
                return redirect('products')

        # ========== تمام کدهای مربوط به سبد خرید حذف شد ==========
        # delete_order_basket, add_nubmer_basket, mines_order_basket, add_basket حذف شدند
        
        if request.POST.get('action') == "add_favorite_product":
            id=request.POST.get('product')
            product=Product.objects.get(id=id)
            user=request.user
            user.favorite_products.add(product)
        
        # add_basket حذف شد
        
        return render(request, self.template_name, {
            'products':Product.objects.only('name','old_price','off','slug','id').annotate(
            price= F('old_price')*(100-F('off'))/100
        ).prefetch_related('images'),
            'slider_image': SliderImage.objects.all(),
            'blogs':Blog.objects.all().order_by('-created')[:3] ,
            # user_order_basket حذف شد
        })
    


# ========== جزئیات محصول ==========
class Detail( DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            Product.objects
            .prefetch_related(
                'images',
                'color',
                'category_main',
                "door_color",
                "body_color",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        categories = product.category_main.all()
        context['price']=product.old_price * (100 - product.off) / 100
        context['products']=Product.objects.filter(category_main__in= categories).only('name','old_price','off','slug','id').annotate(
            price= F('old_price')*(100-F('off'))/100
        ).prefetch_related('images','color')
        context['comments']=Comment.objects.filter(product=product,state='c')
        context['questions']=Question.objects.filter(product=product,state='c')
        # ========== سبد خرید حذف شد ==========
        # context['user_order_basket']=OrderBasket.objects.filter(user=self.request.user).select_related('product0').annotate(price=F('product__old_price')*(100-F('product__off'))/100).aggregate(total_price=Sum(F('number') * F('price')),total_number=Sum(F('number')))   
        
        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        user = request.user
        product = self.get_object()
        
        # ========== add_basket حذف شد ==========
        # if action == "add_basket":
        #     order_basket, created = OrderBasket.objects.get_or_create(user=user)
        #     order_basket.products.add(product)
        #     return redirect('home')
            
        if action == "question":
            question = request.POST.get('question')
            Question.objects.create(user=user, description=question, product=product)
            return redirect('detail', slug=product.slug)
        if action == "comment":
            comment = request.POST.get('comment')
            Comment.objects.create(user=user, description=comment, product=product)
            return redirect('detail', slug=product.slug)
        
        ##
        if request.POST.get('action') == "search_box":
            search_query = request.POST.get('search_input', '').strip()
            if search_query:
                 products = Product.objects.filter(
                    Q(name__icontains=search_query) |
                    Q(introduction__icontains=search_query)|
                    Q(wood_kind__icontains=search_query)|
                    Q(features__title__icontains=search_query)|
                    Q(features__description__icontains=search_query)|
                    Q(category__title__icontains=search_query)|
                    Q(color__color_name__icontains=search_query)
                ).distinct().order_by('-created_at')
                 
            else:
                products = Product.objects.none()
            return render(request, 'home.html', {
            'products': products,
            'search_query':search_query
            })

        # ========== تمام کدهای مربوط به سبد خرید حذف شد ==========
        # delete_order_basket, add_nubmer_basket, mines_order_basket, add_basket, add_product-order حذف شدند
        
        if request.POST.get('action') == "add_favorite_product":
            id=request.POST.get('product')
            product=Product.objects.get(id=id)
            user=request.user
            user.favorite_products.add(product)
        
        # add_product-order حذف شد

        return redirect('detail', slug=product.slug)
        
from datetime import timedelta

import jdatetime
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView

from .models import (
    Order,
    OrderItem,
    DiscountCode,
    HandOverOrder,
    DeliverySettings,
    AddressInfo,
)


def parse_jalali_date(value):
    """
    value example: '1405-04-12'
    """
    year, month, day = map(int, value.split('-'))
    return jdatetime.date(year, month, day)


def get_available_delivery_dates():
    settings = DeliverySettings.objects.first()

    if not settings or not settings.is_active:
        return []

    today = jdatetime.date.today()
    start_date = today + timedelta(days=settings.start_after_days)

    available_dates = []
    current = start_date

    max_scan_days = 365
    scanned_days = 0

    while len(available_dates) < settings.visible_days and scanned_days < max_scan_days:
        if current.isoweekday() != 5:  # جمعه
            daily_count = HandOverOrder.objects.filter(date=current).count()

            if daily_count < settings.max_orders_per_day:
                available_dates.append({
                    'value': current.strftime('%Y-%m-%d'),
                    'label': current.strftime('%Y/%m/%d'),
                })

        current += timedelta(days=1)
        scanned_days += 1

    return available_dates


class Ordering(LoginRequiredMixin, CreateView):
    template_name = 'order_page.html'
    model = Order
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from cart.services import UnifiedCartService
        cart_service = UnifiedCartService.get_cart(self.request)

        context['cart_items'] = cart_service.get_items()
        context['total_price'] = cart_service.get_total_price()
        context['total_items'] = cart_service.get_total_items()
        context['user_addresses'] = AddressInfo.objects.filter(user=self.request.user)
        context['available_dates'] = get_available_delivery_dates()

        return context

    def post(self, request, *args, **kwargs):
        from cart.services import UnifiedCartService
        cart_service = UnifiedCartService.get_cart(request)
        cart_items = cart_service.get_items()

        if not cart_items:
            messages.error(request, 'سبد خرید شما خالی است!')
            return redirect('cart:cart_detail')

        address_id = request.POST.get('address_id')
        delivery_date_value = request.POST.get('delivery_date')
        discount_code_value = request.POST.get('discount_code', '').strip()

        if not address_id:
            messages.error(request, 'لطفا آدرس تحویل را انتخاب کنید.')
            return redirect('ordering')

        if not delivery_date_value:
            messages.error(request, 'لطفا تاریخ تحویل را انتخاب کنید.')
            return redirect('ordering')

        address = get_object_or_404(
            AddressInfo,
            id=address_id,
            user=request.user
        )

        try:
            selected_date = parse_jalali_date(delivery_date_value)
        except Exception:
            messages.error(request, 'تاریخ انتخاب‌شده معتبر نیست.')
            return redirect('ordering')

        settings = DeliverySettings.objects.first()
        if not settings or not settings.is_active:
            messages.error(request, 'سیستم تحویل فعلاً غیرفعال است.')
            return redirect('ordering')

        today = jdatetime.date.today()
        start_date = today + timedelta(days=settings.start_after_days)

        if selected_date < start_date:
            messages.error(request, 'این تاریخ هنوز برای ثبت سفارش باز نشده است.')
            return redirect('ordering')

        if selected_date.isoweekday() == 5:
            messages.error(request, 'روز جمعه برای تحویل فعال نیست.')
            return redirect('ordering')

        total_price = cart_service.get_total_price()
        discount_amount = 0
        final_price = total_price
        discount_obj = None

        try:
            with transaction.atomic():
                current_count = HandOverOrder.objects.select_for_update().filter(
                    date=selected_date
                ).count()

                if current_count >= settings.max_orders_per_day:
                    messages.error(request, 'ظرفیت این روز تکمیل شده است.')
                    return redirect('ordering')

                # =========================
                # تخفیف
                # =========================
                if discount_code_value:
                    try:
                        discount_obj = DiscountCode.objects.select_for_update().get(
                            code__iexact=discount_code_value
                        )

                        # کد باید فعال و معتبر باشد
                        if not discount_obj.is_valid:
                            messages.error(request, 'این کد تخفیف معتبر نیست.')
                            return redirect('ordering')

                        # کاربر نباید قبلاً از این کد استفاده کرده باشد
                        if discount_obj.users.filter(pk=request.user.pk).exists():
                            messages.error(request, 'شما قبلاً از این کد تخفیف استفاده کرده‌اید.')
                            return redirect('ordering')

                        # حداقل مبلغ سفارش
                        if total_price < discount_obj.min_order_amount:
                            messages.error(request, 'مبلغ سفارش به حداقل مبلغ لازم برای این کد نرسیده است.')
                            return redirect('ordering')

                        # محاسبه تخفیف
                        discount_amount = (total_price * discount_obj.percent_off) // 100
                        if discount_amount > discount_obj.max_discount_amount:
                            discount_amount = discount_obj.max_discount_amount

                        final_price = total_price - discount_amount

                    except DiscountCode.DoesNotExist:
                        messages.error(request, 'کد تخفیف معتبر نیست.')
                        return redirect('ordering')

                # =========================
                # ساخت سفارش
                # =========================
                order = Order.objects.create(
                    user=request.user,
                    receiver=address.receiver,
                    phonenumber=address.phonenumber,
                    province=address.province,
                    city=address.city,
                    address=address.address,
                    address_code=address.address_code,
                    date=selected_date,
                    total_price=total_price,
                    discount_amount=discount_amount,
                    final_price=final_price,
                    discount_code=discount_obj,
                    state='unpay',
                )

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        user=request.user,
                        product=item['product'],
                        color=item['color'],
                        number=item['quantity'],
                        price=item['final_price'],
                        body_color=item.get('body_color'),
                        door_color=item.get('door_color'),
                    )

                HandOverOrder.objects.create(
                    order=order,
                    date=selected_date,
                    price=0
                )

                # ثبت اینکه این کاربر از این کد استفاده کرده
                if discount_obj:
                    discount_obj.users.add(request.user)

        except Exception:
            messages.error(request, 'خطا در ثبت سفارش رخ داد.')
            return redirect('ordering')

        messages.success(request, f'سفارش شماره {order.id} ثبت شد.')
        return redirect('payment_method', order.id)


# ========== سبد خرید ==========
# کلاس OrderBasketPage به طور کامل حذف شد - به جای آن از cart app استفاده کن
# class OrderBasketPage(LoginRequiredMixin, ListView):
#     model = OrderBasket
#     template_name = 'orderbasket.html'
#     context_object_name = 'orders'
#     ...


# ========== احراز هویت با OTP ==========


def send_otp(request):

    if request.method == 'POST':

        form = PhoneForm(request.POST)

        if form.is_valid():

            phone = form.cleaned_data['phone']

            # محدودیت
            can_send, error_message = OTP.can_send(phone)

            if not can_send:

                messages.error(
                    request,
                    error_message
                )

                return redirect('send_otp')

            user_exists = CustomUser.objects.filter(
                username=phone
            ).exists()

            otp = OTP.send_otp(phone)

            request.session['otp_phone'] = phone

            request.session['otp_id'] = otp.id

            request.session['is_register'] = not user_exists

            request.session.set_expiry(300)

            return redirect('verify_otp')

    else:

        form = PhoneForm()

    return render(
        request,
        'send_otp.html',
        {
            'form': form
        }
    )





def verify_otp(request):

    phone = request.session.get('otp_phone')

    otp_id = request.session.get('otp_id')

    if not phone or not otp_id:

        messages.error(
            request,
            'ابتدا شماره موبایل را وارد کنید'
        )

        return redirect('send_otp')

    if request.method == 'POST':

        form = OTPForm(request.POST)

        if form.is_valid():

            code = form.cleaned_data['code']

            try:

                with transaction.atomic():

                    otp = OTP.objects.select_for_update().get(
                        id=otp_id,
                        phone=phone
                    )

                    if not otp.is_valid():

                        messages.error(
                            request,
                            'کد تأیید منقضی شده یا نامعتبر است'
                        )

                        return redirect('send_otp')

                    if not otp.check_code(code):

                        remaining = (
                            OTP.MAX_ATTEMPTS - otp.attempts
                        )

                        if remaining <= 0:

                            otp.is_used = True

                            otp.save(
                                update_fields=['is_used']
                            )

                            messages.error(
                                request,
                                'تعداد تلاش بیش از حد مجاز است'
                            )

                            return redirect('send_otp')

                        messages.error(
                            request,
                            'کد اشتباه است'
                        )

                        return redirect('verify_otp')

                    otp.is_used = True

                    otp.save(
                        update_fields=['is_used']
                    )

            except OTP.DoesNotExist:

                messages.error(
                    request,
                    'کد تأیید نامعتبر است'
                )

                return redirect('send_otp')

            user, created = CustomUser.objects.get_or_create(
                username=phone,
                defaults={
                    'is_phone_verified': True
                }
            )

            if not created and not user.is_phone_verified:

                user.is_phone_verified = True

                user.save(
                    update_fields=['is_phone_verified']
                )

            request.session.cycle_key()

            django_login(request, user)

            request.session.pop('otp_phone', None)
            request.session.pop('otp_id', None)

            if created:

                request.session['new_user_id'] = user.id

                return redirect('complete_register')

            messages.success(
                request,
                'با موفقیت وارد شدید'
            )

            return redirect('home')

    else:

        form = OTPForm()

    otp = OTP.objects.get(
        id=otp_id,
        phone=phone
    )

    remaining_seconds = max(
        0,
        OTP.RESEND_COOLDOWN_SECONDS -
        int(
            (
                timezone.now() -
                otp.created_at
            ).total_seconds()
        )
    )

    return render(
        request,
        'verify_otp.html',
        {
            'form': form,
            'phone': phone,
            'cooldown': remaining_seconds,
        }
    )





def resend_otp(request):

    phone = request.session.get('otp_phone')

    if not phone:

        messages.error(
            request,
            'ابتدا شماره موبایل را وارد کنید'
        )

        return redirect('send_otp')

    can_send, error_message = OTP.can_send(phone)

    if not can_send:

        messages.error(
            request,
            error_message
        )

        return redirect('verify_otp')

    otp = OTP.send_otp(phone)

    request.session['otp_id'] = otp.id

    request.session.set_expiry(300)

    messages.success(
        request,
        'کد جدید ارسال شد'
    )

    return redirect('verify_otp')



def complete_register(request):

    # گرفتن user جدید
    user_id = request.session.get('new_user_id')

    if not user_id:

        messages.error(
            request,
            'دسترسی نامعتبر است'
        )

        return redirect('send_otp')

    try:

        user = CustomUser.objects.get(id=user_id)

    except CustomUser.DoesNotExist:

        messages.error(
            request,
            'کاربر یافت نشد'
        )

        return redirect('send_otp')

    # اگر قبلاً کامل شده
    if user.first_name and user.last_name:

        return redirect('home')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']

            user.save()
            
            send_mail(
                subject='ثبت نام کاربر جدید',
            
                message=f"""
            یک کاربر جدید ثبت نام خود را تکمیل کرد.
            
            شماره موبایل:
            {user.username}
            
            نام:
            {user.first_name}
            
            نام خانوادگی:
            {user.last_name}
            
            ایمیل:
            {user.email}
            """,
            
                from_email=None,
            
                recipient_list=[
                    'mahdilotfi249@gmail.com'
                ],
            
                fail_silently=False,
            )
# پاکسازی session
            request.session.pop('new_user_id', None)

            messages.success(
                request,
                'ثبت نام با موفقیت انجام شد'
            )

            return redirect('home')

    else:

        form = RegisterForm()

    return render(request, 'complete_register.html', {
        'form': form,
        'phone': user.username
    })




def logout(request):

    # پاکسازی کامل session
    request.session.flush()

    # logout
    django_logout(request)

    messages.success(
        request,
        'با موفقیت خارج شدید'
    )

    return redirect('send_otp')




class AddAddressinfo(CreateView):
    template_name="add_address_info.html"
    model=AddressInfo
    fields=("user","address","address_code","phonenumber","receiver")
    success_url=reverse_lazy('home')
    
    
from django.contrib.auth.decorators import login_required
@login_required
def add_address(request):

    if request.method == "POST":

        form = AddAddressForm(request.POST)

        if form.is_valid():

            address = form.save(commit=False)

            address.user = request.user

            # استان از روی شهر انتخابی
            address.province = address.city.province

            address.save()

            messages.success(
                request,
                "آدرس با موفقیت ثبت شد."
            )

            return redirect('home')

    else:

        form = AddAddressForm()

    return render(
        request,
        'add_address_info.html',
        {
            'form': form,
        }
    )

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    else:
        form = ProfileForm(instance=request.user)

    context={
    'form': form,
    'current_page':"profile"
    }
    return render(request, 'edit_profile.html', context)


def pay(request):
    return render(request,'pay.html')


class Products(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'xx.html'
    paginate_by = 16

    def get_queryset(self):
        """
        واکشی و اعمال تمامی فیلترها روی محصولات.
        جنگو خروجی این متد را برای صفحه‌بندی استفاده می‌کند.
        """
        # بررسی فیلتر متنی (جستجو از طریق باکس یا از طریق URL متغیر)
        search_query = self.request.GET.get('search_query') or self.kwargs.get('string')
        
        if search_query:
            products = Product.objects.filter(
                Q(name__icontains=search_query) |
                Q(introduction__icontains=search_query) |
                Q(wood_kind__icontains=search_query) |
                Q(features__title__icontains=search_query) |
                Q(features__description__icontains=search_query) |
                Q(category_main__title__icontains=search_query) |
                Q(color__color_name__icontains=search_query)
            ).distinct()
        else:
            products = Product.objects.all()

        # اعمال فیلتر قیمت (در صورت نبودن پارامتر، مقادیر پیش‌فرض بزرگ اعمال می‌شود)
        min_price = self.request.GET.get('rangeMin', '0')
        max_price = self.request.GET.get('rangeMax', '100000000')
        try:
            products = products.annotate(
                price=F('old_price') * (100 - F('off')) / 100
            ).filter(price__gte=int(min_price), price__lte=int(max_price))
        except (ValueError, TypeError):
            products = products.annotate(price=F('old_price') * (100 - F('off')) / 100)

        # اعمال فیلتر نوع چوب
        wood_kinds = []
        wood_mapping = {
            'MDF': 'MDF', 
            'hayglas': 'هایگلاس', 
            'natural': 'چوب طبیعی', 
            'PVC': 'PVC'
        }
        for key, value in wood_mapping.items():
            if self.request.GET.get(key):
                wood_kinds.append(value)
        if wood_kinds:
            products = products.filter(wood_kind__in=wood_kinds)

        # اعمال فیلتر رنگ‌ها
        selected_colors_str = self.request.GET.get('selected_colors')
        if selected_colors_str:
            color_ids = [int(cid) for cid in selected_colors_str.split(',') if cid.isdigit()]
            if color_ids:
                products = products.filter(color__id__in=color_ids).distinct()

        # اعمال مرتب‌سازی محصولات
        sort_action = self.request.GET.get('sort_action', '1')
        if sort_action == '2':
            products = products.order_by('-price')
        elif sort_action == '3':
            products = products.order_by('price')
        elif sort_action == '4':
            products = products.order_by('-stock')
        else:
            products = products.order_by('-created_at')

        # بهینه‌سازی کوئری با only و prefetch_related جهت کاهش لود دیتابیس
        return products.only(
            'name', 'old_price', 'off', 'slug', 'id', 'stock', 'created_at', 'wood_kind', 'category_main'
        ).prefetch_related(
            Prefetch('images', to_attr='cached_images'), 'color'
        )

    def get_context_data(self, **kwargs):
        """
        ارسال تمامی متغیرهای کانتکست مورد نیاز به قالب بدون حذف کدهای شما.
        """
        context = super().get_context_data(**kwargs)
        
        # ساخت کوئری‌استرینگ فیلترها (بدون پارامتر page) جهت الصاق به لینک‌های صفحه‌بندی
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['filter_params'] = query_params.urlencode()

        # هدر، دسته‌بندی‌ها و رنگ‌ها
        context['colors'] = ColorProduct.objects.all()[:9]
        
        # حفظ وضعیت المان‌های فرم فیلتر در ظاهر صفحه
        context['selected_min_price'] = self.request.GET.get('rangeMin', '0')
        context['selected_max_price'] = self.request.GET.get('rangeMax', '100000000')
        context['selected_colors'] = self.request.GET.get('selected_colors', '')
        context['selected_mdf'] = self.request.GET.get('MDF')
        context['selected_hayglas'] = self.request.GET.get('hayglas')
        context['selected_natural'] = self.request.GET.get('natural')
        context['selected_pvc'] = self.request.GET.get('PVC')
        context['current_sort'] = self.request.GET.get('sort_action', '1')
        context['search_query'] = self.request.GET.get('search_query') or self.kwargs.get('string', '')

        # ========== محاسبات مربوط به سبد خرید حذف شد - از cart app و context processor استفاده کن ==========
        # if self.request.user.is_authenticated:
        #     order_basket_result = OrderBasket.objects.filter(
        #         user=self.request.user
        #     ).select_related('product', 'color').annotate(
        #         price=F('product__old_price') * (100 - F('product__off')) / 100
        #     ).aggregate(
        #         total_price=Sum(F('number') * F('price')), 
        #         total_number=Sum(F('number'))
        #     )
        #     context['user_order_basket'] = order_basket_result
        #     context['basket_items'] = OrderBasket.objects.filter(
        #         user=self.request.user
        #     ).select_related('product', 'color').prefetch_related('product__images')[:5]
            
        return context

    def post(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های POST
        """
        action = request.POST.get('action') or request.GET.get('action')
        
        # عملیات سرچ باکس هدر
        if action == "search_box":
            search_input = request.POST.get('search_input', '').strip()
            if search_input:
                return redirect(f"{reverse('products')}?search_query={search_input}")
            else:
                return redirect('products')
                
        # ========== تمام کدهای مربوط به سبد خرید حذف شد ==========
        # delete_order_basket, add_nubmer_basket, mines_order_basket, add_basket حذف شدند
                
        # افزودن محصول به لیست علاقه‌مندی‌ها
        if action == "add_favorite_product":
            product_id = request.POST.get('product')
            request.user.favorite_products.add(Product.objects.get(id=product_id))
            
        # add_basket حذف شد
            
        # بازسازی کوئری‌استرینگ‌های فیلتر قبلی برای ریدایرکت مجدد به صفحه محصولات بدون گم شدن فیلترها
        filter_params = []
        for key, value in request.GET.items():
            if key != 'action' and key != 'page':
                filter_params.append(f"{key}={value}")
                
        sort_action = request.POST.get('sort_action') or request.GET.get('sort_action')
        if sort_action:
            filter_params.append(f"sort_action={sort_action}")
        
        query_string = '&'.join(filter_params)
        redirect_url = reverse('products')
        
        if query_string:
            redirect_url += f'?{query_string}'
        
        return redirect(redirect_url)



from django.contrib.auth.decorators import login_required
@login_required
def payment_method(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if request.method == 'POST':

        method = request.POST.get('payment_method')

        # پرداخت آنلاین
        if method == 'online':
            return redirect(
                'start_payment',
                order.id
            )

        # پرداخت درب منزل
        elif method == 'cod':
            from cart.services import UnifiedCartService
            order.state = 'cash_on_delivery'
            order.generate_tracking_code()
            order.save()
            cart = UnifiedCartService.get_cart(request)
            cart.clear()
            from main.utils import (
                send_order_customer_sms,
                send_order_admin_sms
            )

            send_order_customer_sms(order)
            send_order_admin_sms(order)
            return render(
                    request,
                    'payment_success.html',
                    {
                        'order': order,
                    }
                )

    return render(
        request,
        'payment_method.html',
        {
            'order': order
        }
    )



@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'order_success.html',
        {
            'order': order
        }
    )


class OrderListView(LoginRequiredMixin, ListView):

    model = Order

    template_name = 'order_list.html'

    context_object_name = 'orders'

    paginate_by = 10

    def get_queryset(self):

        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related(
                'order_items'
            )
            .order_by('-id')
        )


class OrderDetailView(
    LoginRequiredMixin,
    DetailView
):

    model = Order

    template_name = 'order_detail.html'

    context_object_name = 'order'

    def get_queryset(self):

        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related(
                'order_items',
                'order_items__product',
                'order_items__color'
            )
        )
    

class AddressListView(LoginRequiredMixin, ListView):
    model = AddressInfo
    template_name = 'addresses.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return AddressInfo.objects.filter(
            user=self.request.user
        ).order_by('-id')


class AddressUpdateView(
    LoginRequiredMixin,
    UpdateView
):
    model = AddressInfo

    form_class = AddressUpdateForm

    template_name = 'address_form.html'

    success_url = reverse_lazy(
        'addresses'
    )

    def get_queryset(self):

        return AddressInfo.objects.filter(
            user=self.request.user
        )


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = AddressInfo

    template_name = 'address_delete.html'
    success_url = reverse_lazy('addresses')

    def get_queryset(self):
        return AddressInfo.objects.filter(
            user=self.request.user
        )
    


class FavoriteProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'favorite_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return self.request.user.favorite_products.all().prefetch_related(
            'images'
        )

@login_required
def toggle_favorite(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if request.user.favorite_products.filter(
        id=product.id
    ).exists():

        request.user.favorite_products.remove(product)

    else:

        request.user.favorite_products.add(product)

    return redirect(request.META.get('HTTP_REFERER', '/'))



class UserActivityView(LoginRequiredMixin, TemplateView):
    template_name = 'user_activity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comments'] = (
            Comment.objects
            .filter(user=self.request.user)
            .select_related('product')
            .order_by('-created_at')
        )

        context['questions'] = (
            Question.objects
            .filter(user=self.request.user)
            .select_related(
                'product',
                'answer'
            )
            .order_by('-created_at')
        )

        return context
    



class BlogListView(ListView):

    model = Blog

    template_name = 'blog_list.html'

    context_object_name = 'blogs'

    paginate_by = 12

    queryset = Blog.objects.order_by(
        '-created'
    )


class BlogDetailView(DetailView):

    model = Blog

    template_name = 'blog_detail.html'

    context_object_name = 'blog'

    slug_field = 'slug'

    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):

        obj = super().get_object(queryset)

        Blog.objects.filter(
            pk=obj.pk
        ).update(
            views=F('views') + 1
        )

        obj.refresh_from_db()

        return obj



class StartPaymentView(LoginRequiredMixin,View):


    def get(self,request,pk):
    
        order = get_object_or_404(
            Order,
            id=pk,
            user=request.user
        )
    
        if order.state == 'payed':
    
            return HttpResponse(
                'این سفارش قبلاً پرداخت شده است.'
            )
    
        callback_url = (
            request.build_absolute_uri(
                reverse(
                    'verify_payment'
                )
            )
        )
    
        data = {
    
            "merchant_id":
            settings.ZARINPAL_MERCHANT_ID,
    
            "amount":
            int(
                order.final_price
            ),
    
            "callback_url":
            callback_url,
    
            "description":
            f"Order #{order.id}",
        }
    
        try:
    
            response = requests.post(
                "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
                json=data,
                timeout=30
            )
    
            result = response.json()
    
            print(result)
    
            if (
                result.get(
                    'data',
                    {}
                ).get(
                    'code'
                ) == 100
            ):
    
                authority = (
                    result[
                        'data'
                    ][
                        'authority'
                    ]
                )
    
                order.authority = (
                    authority
                )
    
                order.state = (
                    'paying'
                )
    
                order.save()
    
                return redirect(
                    f"https://sandbox.zarinpal.com/pg/StartPay/{authority}"
                )
    
            return HttpResponse(
                f"خطا در ایجاد پرداخت : {result}"
            )
    
        except Exception as e:
    
            return HttpResponse(
                f"خطا در ارتباط با زرین پال : {str(e)}"
            )
    
from cart.services import UnifiedCartService
from .utils import (
send_order_customer_sms,
send_order_admin_sms
)
class VerifyPaymentView(LoginRequiredMixin,View):


    def get(self,request):
    
        authority = (
            request.GET.get(
                'Authority'
            )
        )
    
        status = (
            request.GET.get(
                'Status'
            )
        )
    
        if not authority:
    
            return HttpResponse(
                'Authority یافت نشد.'
            )
    
        order = get_object_or_404(
            Order,
            authority=authority
        )
    
        if status != 'OK':
    
            order.state = (
                'unpay'
            )
    
            order.save()
    
            return render(
                request,
                'payment_failed.html',
                {
                    'order': order,
                }
            )
                
        data = {
    
            "merchant_id":
            settings.ZARINPAL_MERCHANT_ID,
    
            "amount":
            int(
                order.final_price
            ),
    
            "authority":
            authority,
        }
    
        try:
    
            response = requests.post(
                "https://sandbox.zarinpal.com/pg/v4/payment/verify.json",
                json=data,
                timeout=30
            )
    
            result = response.json()
    
            print(result)
    
            if (
                result.get(
                    'data',
                    {}
                ).get(
                    'code'
                ) == 100
            ):
    
                order.state = (
                    'payed'
                )
    
                order.ref_id = str(
                    result[
                        'data'
                    ][
                        'ref_id'
                    ]
                )
    
                order.generate_tracking_code()
    
                order.save()
    
                cart = (
                    UnifiedCartService
                    .get_cart(
                        request
                    )
                )
    
                cart.clear()
    
                try:
    
                    send_order_customer_sms(
                        order
                    )
    
                except Exception as e:
    
                    print(
                        "Customer SMS Error:",
                        e
                    )
    
                try:
    
                    send_order_admin_sms(
                        order
                    )
    
                except Exception as e:
    
                    print(
                        "Admin SMS Error:",
                        e
                    )
    
                return render(
                    request,
                    'payment_success.html',
                    {
                        'order': order,
                    }
                )
    
            order.state = (
                'unpay'
            )
    
            order.save()
    
            return render(
                request,
                'payment_failed.html',
                {
                    'order': order,
                }
            )
    
        except Exception as e:
    
            return HttpResponse(
                f"خطا در تایید پرداخت : {str(e)}"
            )
    
    
        


def payment_intro(request):
    return render(request, 'payment_intro.html')

def delivery_info(request):
    return render(request, 'delivery_info.html')


def shipping_cost(request):
    return render(request, 'shipping_cost.html')



def return_policy(request):
    return render(request, 'return_policy.html')

# صفحه سوالات متداول
def faq(request):
    return render(request, 'faq.html')





@login_required(login_url='login')
def order_tracking(request):
    """
    پیگیری سفارش
    """
    tracking_code = request.GET.get('tracking_code')
    order = None
    orders = None
    
    if tracking_code:
        # جستجو با کد پیگیری یا شماره سفارش
        try:
            if tracking_code.startswith('RK-'):
                # جستجو با کد پیگیری
                order = Order.objects.filter(
                    tracking_code=tracking_code,
                    user=request.user
                ).first()
            else:
                # جستجو با شماره سفارش
                order = Order.objects.filter(
                    id=tracking_code,
                    user=request.user
                ).first()
                
            # اگر پیدا نشد، همه سفارشات کاربر را نشان بده
            if not order:
                orders = Order.objects.filter(user=request.user).order_by('-created_at')
        except (ValueError, TypeError):
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        # نمایش لیست سفارشات کاربر
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'order': order,
        'orders': orders,
    }
    
    return render(request, 'order_tracking.html', context)



# راهنمای خرید
def shopping_guide(request):
    return render(request, 'shopping_guide.html')


# قوانین و مقررات
def terms(request):
    return render(request, 'terms.html')



def about_us(request):
    """
    صفحه درباره ما
    """
    return render(request, 'about_us.html')