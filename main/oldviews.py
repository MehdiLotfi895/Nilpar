# views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout
from django.utils import timezone
from django.db.models import Q ,F ,Sum,DecimalField, Value,Prefetch
from .models import Product, Order, HandOverOrder, AddressInfo, CustomUser, OTP ,Question ,Comment,Header_top,CategoryMain,SliderImage,Blog,OrderBasket,ColorProduct,OrderItem,AdItem,AdSection
from .forms import PhoneForm, OTPForm, RegisterForm,AddAddressForm,ProfileForm
from django.db.models.functions import Coalesce
from django.db.models.expressions import ExpressionWrapper, CombinedExpression
from django.db import models
from django.urls import reverse
from django.core.paginator import Paginator
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
        context['header_content']=Header_top.objects.filter(state='active').first()
        context['main_category']=CategoryMain.objects.prefetch_related('secondary_category').all().order_by('-id')
        context['slider_image']=SliderImage.objects.all()
        context['blogs']=Blog.objects.all().order_by('-created')[:3]
        context['ad_section_first']=AdSection.objects.exclude(state="repose",title="").prefetch_related('image').select_related('category_main').first()
        context['ad_section_second']=AdSection.objects.filter(state='active',title__isnull=True).prefetch_related('image').select_related('category_main').first()
        if self.request.user.is_authenticated:
            context['user_order_basket']=OrderBasket.objects.filter(user=self.request.user).select_related('product','color').prefetch_related('product__images').annotate(price=F('product__old_price')*(100-F('product__off'))/100).aggregate(total_price=Sum(F('number') * F('price')),total_number=Sum(F('number')))   

        return context
    
    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == "search_box":
            search_query = request.POST.get('search_input', '').strip()
            return redirect('products',search_query)

        if request.POST.get('action') == 'delete_order_basket':
            product_order= request.POST.get('product_order_basket')
            user = request.user
            color=request.POST.get('color')
            OrderBasket.objects.filter(user=user,product=product_order,color=color).delete()
        
        if request.POST.get('action') == 'add_nubmer_basket':
            product_order= Product.objects.get(id=request.POST.get('product_order_basket'))
            user = request.user
            color=ColorProduct.objects.get(id=request.POST.get('color'))
            number=OrderBasket.objects.filter(user=user,product=product_order,color=color).first().number
            int=product_order.max_number_order
            if number+1 <= int:
                OrderBasket.objects.filter(user=user,product=product_order,color=color).update(number=number+1)
        
        if request.POST.get('action') == 'mines_order_basket':
            product_order= Product.objects.get(id=request.POST.get('product_order_basket'))
            user = request.user
            color=ColorProduct.objects.get(id=request.POST.get('color'))
            number=OrderBasket.objects.filter(user=user,product=product_order,color=color).first().number
            if number-1 > 0:
                OrderBasket.objects.filter(user=user,product=product_order,color=color).update(number=number-1)
        if request.POST.get('action') == "add_favorite_product":
            id=request.POST.get('product')
            product=Product.objects.get(id=id)
            user=request.user
            user.favorite_products.add(product)
        
        if request.POST.get('action') == "add_basket":
            user=request.user
            id=request.POST.get('product')
            product=Product.objects.get(id=id)
            user.order_basket.add(product)
            
        return render(request, self.template_name, {
            'products':Product.objects.only('name','old_price','off','slug','id').annotate(
            price= F('old_price')*(100-F('off'))/100
        ).prefetch_related('images'),
            'header_content':Header_top.objects.filter(state='active').first() ,
            'main_category':CategoryMain.objects.prefetch_related('secondary_category').all().order_by('-id') ,
            'slider_image': SliderImage.objects.all(),
            'blogs':Blog.objects.all().order_by('-created')[:3] ,
            'user_order_basket':OrderBasket.objects.filter(user=self.request.user).annotate(price=F('product__old_price')*(100-F('product__off'))/100).prefetch_related('product__images').aggregate(total_price=Sum(F('number') * F('price')),total_number=Sum(F('number')))
        })
    


# ========== جزئیات محصول ==========
class Detail(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'detail.html'
    slug_field = 'slug'          # این خط رو اضافه کن (می‌تونه اختیاری باشه چون default='slug' هست)
    slug_url_kwarg = 'slug'      # این هم اختیاری
    

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_content']=Header_top.objects.filter(state='active').first()
        context['main_category']=CategoryMain.objects.prefetch_related('secondary_category').all().order_by('-id')
        categories=self.get_object().category_main.all()
        context['products']=Product.objects.filter(category_main__in= categories).only('name','old_price','off','slug','id').annotate(
            price= F('old_price')*(100-F('off'))/100
        ).prefetch_related('images','color')
        context['user_order_basket']=OrderBasket.objects.filter(user=self.request.user).select_related('product0').annotate(price=F('product__old_price')*(100-F('product__off'))/100).aggregate(total_price=Sum(F('number') * F('price')),total_number=Sum(F('number')))   
        return context
    
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        user = request.user
        product = self.get_object()
        if action == "add_basket":
            order_basket, created = OrderBasket.objects.get_or_create(user=user)
            order_basket.products.add(product)
            return redirect('home')
        if action == "question":
            question = request.POST.get('question')
            Question.objects.create(user=user, description=question, product=product)
            return redirect('detail', slug=product.slug)   # تغییر این خط: به جای pk از slug استفاده کن
        if action == "comment":
            comment = request.POST.get('comment')
            Comment.objects.create(user=user, description=comment, product=product)
            return redirect('detail', slug=product.slug)   # تغییر این خط
        
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
                products = Product.objects.none()  # خالی اگه چیزی وارد نشده
            return render(request, 'home.html', {
            'products': products,
            'search_query':search_query
            })

        if request.POST.get('action') == 'delete_order_basket':
            product_order= request.POST.get('product_order_basket')
            user = request.user
            color=request.POST.get('color')
            OrderBasket.objects.filter(user=user,product=product_order,color=color).delete()
        
        if request.POST.get('action') == 'add_nubmer_basket':
            product_order= Product.objects.get(id=request.POST.get('product_order_basket'))
            user = request.user
            color=ColorProduct.objects.get(id=request.POST.get('color'))
            number=OrderBasket.objects.filter(user=user,product=product_order,color=color).first().number
            integer=product_order.max_number_order
            if number+1 <= integer:
                OrderBasket.objects.filter(user=user,product=product_order,color=color).update(number=number+1)
        
        if request.POST.get('action') == 'mines_order_basket':
            product_order= Product.objects.get(id=request.POST.get('product_order_basket'))
            user = request.user
            color=ColorProduct.objects.get(id=request.POST.get('color'))
            number=OrderBasket.objects.filter(user=user,product=product_order,color=color).first().number
            if number-1 > 0:
                OrderBasket.objects.filter(user=user,product=product_order,color=color).update(number=number-1)
        if request.POST.get('action') == "add_favorite_product":
            id=request.POST.get('product')
            product=Product.objects.get(id=id)
            user=request.user
            user.favorite_products.add(product)
        
        if request.POST.get('action') == "add_basket":
            user=request.user
            id=request.POST.get('product')
            product=Product.objects.get(id=id)
            user.order_basket.add(product)
        
        if request.POST.get('action') == 'add_product-order':
            user=request.user
            product=self.get_object()
            number= int(request.POST.get('quantity'))
            max=product.max_number_order
            color_name=request.POST.get('product_color')
            color=ColorProduct.objects.get(color_name=color_name)
            stock=product.stock
            if number >= 1 and number <= max and stock >= number:
                print(1)
                order_basket,created=OrderBasket.objects.get_or_create(user=user,product=product,color=color,defaults={'number':number})
                if not created:
                    print(2)
                    new_number=number+order_basket.number
                    if new_number <=max:
                        print(3)
                        order_basket.number = new_number
                        order_basket.save()

        return redirect('detail', slug=product.slug)
        
    
# ========== سفارش ==========
class Ordering(LoginRequiredMixin, CreateView):
    template_name = 'order_page.html'
    model = Order
    success_url = reverse_lazy('home')
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket_orders= OrderBasket.objects.filter(user=self.request.user).annotate(price=F('product__old_price')*(100 - F('product__off')/100))
        context['basket_orders']=basket_orders
        
        if  basket_orders:
            context['total_price'] = sum(p.price for p in basket_orders)
            context['products_count'] = sum(p.number for p in basket_orders)
            context['date_pack'] = HandOverOrder.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        address_id = request.POST.get('address_id')
        delivery_time_id = request.POST.get('delivery_time_id')
        
        if not address_id:
            return redirect('ordering')
        
        ob = request.user.address.get(id=address_id)
        address = ob.address
        address_code = ob.address_code
        phonenumber = ob.phonenumber
        receiver = ob.receiver
        city=ob.city
        province=ob.province

        delivery_time = HandOverOrder.objects.get(id=delivery_time_id)
        date = delivery_time.date
        clock = delivery_time.clock
        
        baskets = request.user.order_basket.all()
        
        if request.user.order_basket.first():
            order = Order.objects.create(
                user=request.user,
                address=address,
                address_code=address_code,
                phonenumber=phonenumber,
                receiver=receiver,
                city=city,
                province=province,
                date=date,
                clock=clock,
            )
            for item in baskets:
                OrderItem.objects.create(
                    product=item.product,
                    number=item.number,
                    color=item.color,
                    user=item.user,
                    order=order
                )
        
        return redirect('home')


# ========== سبد خرید ==========
class OrderBasketPage(LoginRequiredMixin, ListView):
    model = OrderBasket
    template_name = 'orderbasket.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        user = self.request.user
        return OrderBasket.objects.filter(user=user)
        
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_content']=Header_top.objects.filter(state='active').first()
        context['main_category']=CategoryMain.objects.prefetch_related('secondary_category').all()
        total_price=0
        total_off=0
        total_number=0
        orders=OrderBasket.objects.filter(user=self.request.user)
        for order in orders:
            total_number+=order.number
            total_price+=order.product.old_price*order.number
            total_off+=order.product.off*order.product.old_price/100*order.number
        
        total_new_price=total_price - total_off
        context['total_price']=total_price
        context['total_off']=int(total_off)
        context['total_number']=total_number
        context['total_new_price']=int(total_new_price)
        return context


# ========== احراز هویت با OTP ==========

def send_otp(request):
    """مرحله ۱: دریافت شماره و ارسال کد"""
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            
            # چک کن آیا کاربر وجود داره
            user_exists = CustomUser.objects.filter(username=phone).exists()
            
            # ارسال کد OTP
            otp = OTP.send_otp(phone)
            
            # ذخیره در سشن
            request.session['otp_phone'] = phone
            request.session['otp_id'] = otp.id
            request.session['is_register'] = not user_exists
            return redirect('verify_otp')
    else:
        form = PhoneForm()
    
    return render(request, 'send_otp.html', {'form': form})


def verify_otp(request):
    """مرحله ۲: تأیید کد OTP"""
    phone = request.session.get('otp_phone')
    otp_id = request.session.get('otp_id')
    is_register = request.session.get('is_register', False)
    
    if not phone:
        messages.error(request, "لطفا شماره موبایل خود را وارد کنید")
        return redirect('send_otp')
    
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            
            try:
                otp = OTP.objects.get(id=otp_id, phone=phone, code=code)
            except OTP.DoesNotExist:
                messages.error(request, "کد تأیید نامعتبر است")
                return redirect('verify_otp')
            
            if not otp.is_valid():
                messages.error(request, "کد منقضی شده است")
                return redirect('send_otp')
            
            otp.is_used = True
            otp.save()
            
            del request.session['otp_id']
            
            if is_register:
                return redirect('complete_register')
            else:
                user = CustomUser.objects.get(username=phone)
                django_login(request, user)
                return redirect('home')
    else:
        form = OTPForm()
    
    return render(request, 'verify_otp.html', {
        'form': form,
        'phone': phone,
        'resend_url': 'send_otp'
    })


def complete_register(request):
    """مرحله ۳: تکمیل ثبت‌نام"""
    phone = request.session.get('otp_phone')
    
    if not phone:
        messages.error(request, "لطفا شماره موبایل خود را وارد کنید")
        return redirect('send_otp')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            
            user = CustomUser.objects.create_user(
                username=phone,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            
            # پاک کردن سشن
            del request.session['otp_phone']
            if 'is_register' in request.session:
                del request.session['is_register']
            
            django_login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'complete_register.html', {
        'form': form,
        'phone': phone
    })


def logout(request):
    django_logout(request)
    return redirect('send_otp')




class AddAddressinfo(CreateView):
    template_name="add_address_info.html"
    model=AddressInfo
    fields=("user","address","address_code","phonenumber","receiver")
    success_url=reverse_lazy('home')
    
    
from django.shortcuts import render, redirect

def add_address(request):
    if request.method == "POST":
        form = AddAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('home')
    else:
        form = AddAddressForm()

    return render(request, 'add_address_info.html', {'form': form})


def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    else:
        form = ProfileForm(instance=request.user)

    context={'header_content':Header_top.objects.filter(state='active').first(),
    'main_category':CategoryMain.objects.prefetch_related('secondary_category').all().order_by('-id'),
    'form': form
    }
    return render(request, 'edit_profile.html', context)


def pay(request):
    return render(request,'pay.html')


class Products(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'xx.html'
    paginate_by = 4  # صفحه‌بندی خودکار جنگو (۴ محصول در هر صفحه)

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
        context['header_content'] = Header_top.objects.filter(state='active').first()
        context['main_category'] = CategoryMain.objects.prefetch_related(
            'secondary_category'
        ).all().order_by('-id')
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

        # محاسبات مربوط به سبد خرید کاربر لاگین شده
        if self.request.user.is_authenticated:
            order_basket_result = OrderBasket.objects.filter(
                user=self.request.user
            ).select_related('product', 'color').annotate(
                price=F('product__old_price') * (100 - F('product__off')) / 100
            ).aggregate(
                total_price=Sum(F('number') * F('price')), 
                total_number=Sum(F('number'))
            )
            context['user_order_basket'] = order_basket_result
            context['basket_items'] = OrderBasket.objects.filter(
                user=self.request.user
            ).select_related('product', 'color').prefetch_related('product__images')[:5]
            
        return context

    def post(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های POST شامل مدیریت سبد خرید، افزودن به علاقه‌مندی‌ها و باکس سرچ.
        """
        action = request.POST.get('action') or request.GET.get('action')
        
        # عملیات سرچ باکس هدر
        if action == "search_box":
            search_input = request.POST.get('search_input', '').strip()
            if search_input:
                return redirect(f"{reverse('products')}?search_query={search_input}")
            else:
                return redirect('products')
                
        # حذف از سبد خرید
        elif action == 'delete_order_basket':
            product_id = request.POST.get('product_order_basket')
            color_id = request.POST.get('color')
            OrderBasket.objects.filter(user=request.user, product_id=product_id, color_id=color_id).delete()
        
        # افزایش تعداد کالا در سبد خرید
        elif action == 'add_nubmer_basket':
            product_id = request.POST.get('product_order_basket')
            color_id = request.POST.get('color')
            product_order = Product.objects.get(id=product_id)
            order = OrderBasket.objects.filter(user=request.user, product=product_order, color_id=color_id).first()
            if order and order.number + 1 <= product_order.max_number_order:
                order.number += 1
                order.save()
        
        # کاهش تعداد کالا در سبد خرید
        elif action == 'mines_order_basket':
            product_id = request.POST.get('product_order_basket')
            color_id = request.POST.get('color')
            order = OrderBasket.objects.filter(user=request.user, product_id=product_id, color_id=color_id).first()
            if order and order.number - 1 > 0:
                order.number -= 1
                order.save()
                
        # افزودن محصول به لیست علاقه‌مندی‌ها
        elif action == "add_favorite_product":
            product_id = request.POST.get('product')
            request.user.favorite_products.add(Product.objects.get(id=product_id))
            
        # افزودن مستقیم کالا به سبد خرید
        elif action == "add_basket":
            product_id = request.POST.get('product')
            request.user.order_basket.add(Product.objects.get(id=product_id))
            
        # بازسازی کوئری‌استرینگ‌های فیلتر قبلی برای ریدایرکت مجدد به صفحه محصولات بدون گم شدن فیلترها
        filter_params = []
        for key, value in request.GET.items():
            if key != 'action' and key != 'page':  # پارامتر صفحه در لود جدید به صفحه ۱ می‌رود یا فیلتر جدید می‌گیرد
                filter_params.append(f"{key}={value}")
                
        sort_action = request.POST.get('sort_action') or request.GET.get('sort_action'

)
        if sort_action:
            filter_params.append(f"sort_action={sort_action}")
        
        query_string = '&'.join(filter_params)
        redirect_url = reverse('products')
        
        if query_string:
            redirect_url += f'?{query_string}'
        
        return redirect(redirect_url)