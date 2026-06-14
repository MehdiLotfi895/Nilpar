from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timedelta
import random
import string
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
    EmailValidator,
    URLValidator,
    FileExtensionValidator,
    ProhibitNullCharactersValidator,
)
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels
import jdatetime
from autoslug import AutoSlugField
from django.utils.text import slugify
from iranian_cities.fields import ProvinceField, CityField
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
import secrets
import string


class Feature(models.Model):
    title = models.CharField(
        max_length=300,
        verbose_name=_('title')
    )
    description = models.CharField(
        max_length=300,
        verbose_name=_('description')
    )
    created = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name=_('created')
    )

    def __str__(self):
        return f"{self.title}, {self.description}"

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')

class CategorySecondary(models.Model):
    title=models.CharField(max_length=300)
    created = jmodels.jDateField(
        auto_now_add=True,
        verbose_name=_('created')
    )
    image=models.ImageField(
        upload_to='secondaty_category_image/',
        verbose_name=_('image'),
        null=True,
        blank=True
    )
    def __str__(self):
        return self.title

class CategoryMain(models.Model):
    title = models.CharField(
        max_length=300,
        verbose_name=_('title')
    )
    created = jmodels.jDateField(
        auto_now_add=True,
        verbose_name=_('created')
    )
    image=models.ImageField(upload_to='main_category_image/',
        verbose_name=_('image'),null=True,blank=True)
    secondary_category=models.ManyToManyField(CategorySecondary,related_name='categories_main')
    icone=models.CharField(max_length=300,null=True,blank=True)
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class ColorProduct(models.Model):
    color_name=models.CharField(max_length=300,verbose_name=_('color'))
    color_code=models.CharField(max_length=10,null=True,blank=True)

    class Meta:
        verbose_name = _('color_products')
        verbose_name_plural = _('color_products')


    def __str__(self):
        return f"{self.color_name} ,{self.color_code}"
    
class Product(models.Model):
    COLOR_TYPE_CHOICES = (
    ('single', 'تک رنگ'),
    ('double', 'دو رنگ'),
)

    color_type = models.CharField(
        max_length=10,
        choices=COLOR_TYPE_CHOICES,
        default='single'
    )
    name = models.CharField(
        max_length=300,
        verbose_name=_('name')
    )
    introduction = models.TextField(
        verbose_name=_('introduction')
    )
    features = models.ManyToManyField(
        Feature,
        blank=True,
        related_name='products',
        verbose_name=_('features')
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name=_('weight')
    )
    dimensions = models.CharField(
        max_length=150,
        verbose_name=_('dimensions')
    )
    category_main = models.ManyToManyField(
        CategoryMain,
        blank=True,
        related_name='products',
        verbose_name=_('main-category')
    )
    category_second = models.ManyToManyField(
        CategorySecondary,
        blank=True,
        related_name='products',
        verbose_name=_('secondary-category')
    )
    more_details = models.TextField(
        verbose_name=_('more_details')
    )
    old_price=models.PositiveBigIntegerField(
        verbose_name=_('oldprice'),
        default=0,
    )
    # price = models.PositiveBigIntegerField(
    #     verbose_name=_('price')
    # )
    stock = models.PositiveSmallIntegerField(
        verbose_name=_('stock')
    )
    wood_kind = models.CharField(
        max_length=300,
        default='MDF',
        verbose_name=_('wood_kind')
    )
    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name=_('created_at')
    )
    updated_at = jmodels.jDateTimeField(
        auto_now=True,
        verbose_name=_('updated_at')
    )
    off=models.PositiveSmallIntegerField(
        verbose_name=_('off'),
        default=0,
        validators=[
            MinValueValidator(0),
           MaxValueValidator(50)
        ])
    color=models.ManyToManyField(ColorProduct,related_name='products',
        verbose_name=_('color') )
    
    body_color=models.ManyToManyField(ColorProduct,related_name='products_body_color',verbose_name=_('رنگ بدنه'))

    door_color=models.ManyToManyField(ColorProduct,related_name='products_door_color',verbose_name=_('رنگ در'))
    
    accessories = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='used_as_accessory_for',
        verbose_name='لوازم جانبی'
    )

    slug = models.SlugField(
        max_length=255,   # کمی بلندتر از name
        unique=True,
        blank=True,
        verbose_name=_('slug')
    )
    max_number_order=models.PositiveSmallIntegerField(default=3)
    
    def save(self, *args, **kwargs):
       if not self.slug:
           # ساخت اسلاگ از روی name با پشتیبانی از فارسی
           self.slug = slugify(self.name, allow_unicode=True)
           
           # مدیریت تکراری بودن اسلاگ
           original_slug = self.slug
           counter = 1
           while Product.objects.filter(slug=self.slug).exists():
               self.slug = f"{original_slug}-{counter}"
               counter += 1
               
       super().save(*args, **kwargs)
    def __str__(self):
        return f"Name: {self.name}"

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')





class Comment(models.Model):
    comment_state = (
        ('c', _('confirmed')),
        ('p', _('pending')),
        ('r', _('rejected')),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    description = models.TextField(
        verbose_name=_('description')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='comments'
    )
    state = models.CharField(
        max_length=1,
        choices=comment_state,
        default='p',
        verbose_name=_('state')
    )
    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name=_('created_at')
    )

    def __str__(self):
        return f"Product: {self.product}, User: {self.user}"

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Question(models.Model):
    question_state = (
        ('c', _('confirmed')),
        ('p', _('pending')),
        ('r', _('rejected')),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    description = models.TextField(
        verbose_name=_('description')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    state = models.CharField(
        max_length=1,
        choices=question_state,
        default='p',
        verbose_name=_('state')
    )
    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name=_('created_at')
    )

    def __str__(self):
        return f"User: {self.user}, Post: {self.description}"

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')


class Answer(models.Model):
    admin_answer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('admin_answer')
    )
    description = models.TextField(
        verbose_name=_('description')
    )
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_('question')
    )
    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name=_('created_at')
    )
    updated_at = jmodels.jDateField(
        auto_now=True,
        verbose_name=_('updated_at')
    )

    def __str__(self):
        return f"Description: {self.description}, Question: {self.question}"

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')


class Image_profile_product(models.Model):
    image = models.ImageField(
        upload_to='products_image/',
        verbose_name=_('image')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('images')
    )

    def __str__(self):
        return f"{self.product}"

    class Meta:
        verbose_name = _('product_image')
        verbose_name_plural = _('product_images')


class AddressInfo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='address',
        verbose_name=_('user')
    )
    province = ProvinceField(verbose_name="استان",null=True,blank=True)
    city = CityField(verbose_name="شهر",null=True,blank=True)
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('address')
    )
    address_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name=_('address_code')
    )
    phonenumber = models.CharField(
        max_length=11,
        verbose_name=_('phone_number')
    )
    receiver = models.CharField(
        max_length=300,
        verbose_name=_('receiver')
    )
    updated_at = jmodels.jDateTimeField(
        auto_now=True,
        verbose_name=_('updated_at')
    )
    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name=_('created_at')
    )

    def __str__(self):
        return f"{self.user}, {self.address}"

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')


class Order(models.Model):
    order_state = (
        ('payed', _('payed')),
        ('paying', _('paying')),
        ('unpay', _('unpaid')),
        ('cash_on_delivery', _('cash_on_delivery')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date = jmodels.jDateField(verbose_name=_('delivery_date'))

    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    state = models.CharField(max_length=16, choices=order_state, default='unpay')

    province = ProvinceField(null=True, blank=True)
    city = CityField(null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    address_code = models.CharField(max_length=10, null=True, blank=True)

    phonenumber = models.CharField(max_length=11, null=True, blank=True)
    receiver = models.CharField(max_length=300, null=True, blank=True)

    authority = models.CharField(max_length=200, null=True, blank=True)
    ref_id = models.CharField(max_length=200, null=True, blank=True)

    # =========================
    # 💰 قیمت‌ها (مهم‌ترین بخش)
    # =========================

    total_price = models.PositiveBigIntegerField(default=0)  # قیمت اصلی

    discount_amount = models.PositiveBigIntegerField(default=0)  # مقدار تخفیف

    final_price = models.PositiveBigIntegerField(default=0)  # مبلغ نهایی (برای درگاه)

    discount_code = models.ForeignKey(
        'DiscountCode',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )

    tracking_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def generate_tracking_code(self):
        if not self.tracking_code:
            self.tracking_code = f"RK-{self.id:06d}"

    def __str__(self):
        return f"Order #{self.id} - {self.user}"
    
    
  

class OrderItem(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    number = models.PositiveSmallIntegerField()

    color = models.ForeignKey(
        ColorProduct,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orderitems_single'
    )

    body_color = models.ForeignKey(
        ColorProduct,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orderitems_body'
    )

    door_color = models.ForeignKey(
        ColorProduct,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orderitems_door'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    price = models.PositiveBigIntegerField(default=0)

    @property
    def total_price(self):
        return self.price * self.number
    
# class OrderBasket(models.Model):
#     products = models.ManyToManyField(
#         Product,
#         verbose_name=_('products')
#     )
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='orderbasket',
#         verbose_name=_('user')
#     )
#     created_at = jmodels.jDateTimeField(
#         auto_now_add=True,
#         verbose_name=_('created_at')
#     )
#     updated_at = jmodels.jDateTimeField(
#         auto_now=True,
#         verbose_name=_('updated_at')
#     )

#     def __str__(self):
#         return f"{self.user}"

#     class Meta:
#         verbose_name = _('order_basket')
#         verbose_name_plural = _('order_baskets')


class DeliverySettings(models.Model):
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )

    start_after_days = models.PositiveSmallIntegerField(
        default=10,
        verbose_name='شروع از چند روز بعد'
    )

    visible_days = models.PositiveSmallIntegerField(
        default=10,
        verbose_name='تعداد روزهای قابل نمایش'
    )

    max_orders_per_day = models.PositiveSmallIntegerField(
        default=10,
        verbose_name='حداکثر سفارش روزانه'
    )

    class Meta:
        verbose_name = 'تنظیمات تحویل'
        verbose_name_plural = 'تنظیمات تحویل'

    def __str__(self):
        return 'تنظیمات تحویل'


class HandOverOrder(models.Model):
    date = jmodels.jDateField(
        verbose_name=_('date')
    )

    order = models.OneToOneField(
        'Order',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('order')
    )

    price = models.PositiveIntegerField(
        default=0,
        verbose_name=_('price')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    class Meta:
        verbose_name = _('handover_order')
        verbose_name_plural = _('handover_orders')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.date} - {self.order}'



class OTP(models.Model):

    phone = models.CharField(
        max_length=11,
        db_index=True
    )

    code = models.CharField(
        max_length=128
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_used = models.BooleanField(
        default=False
    )

    attempts = models.PositiveIntegerField(
        default=0
    )

    class Meta:

        ordering = ['-created_at']

    # =========================
    # SETTINGS
    # =========================

    OTP_EXPIRE_MINUTES = 2

    MAX_ATTEMPTS = 5

    RESEND_COOLDOWN_SECONDS = 120

    DAILY_LIMIT = 10

    # =========================
    # OTP VALID
    # =========================

    def is_valid(self):

        expire_time = self.created_at + timedelta(
            minutes=self.OTP_EXPIRE_MINUTES
        )

        return (
            timezone.now() < expire_time
            and not self.is_used
            and self.attempts < self.MAX_ATTEMPTS
        )

    # =========================
    # GENERATE CODE
    # =========================

    @staticmethod
    def generate_code():

        return ''.join(
            secrets.choice(string.digits)
            for _ in range(6)
        )

    # =========================
    # CHECK CODE
    # =========================

    def check_code(self, raw_code):

        self.attempts += 1

        self.save(update_fields=['attempts'])

        return check_password(raw_code, self.code)

    # =========================
    # CAN SEND
    # =========================

    @classmethod
    def can_send(cls, phone):

        now = timezone.now()

        # cooldown
        recent_otp = cls.objects.filter(
            phone=phone
        ).first()

        if recent_otp:

            cooldown = recent_otp.created_at + timedelta(
                seconds=cls.RESEND_COOLDOWN_SECONDS
            )

            if now < cooldown:

                remaining = int(
                    (cooldown - now).total_seconds()
                )

                return (
                    False,
                    f'{remaining} ثانیه دیگر تلاش کنید'
                )

        # daily limit
        today = now - timedelta(days=1)

        sent_count = cls.objects.filter(
            phone=phone,
            created_at__gte=today
        ).count()

        if sent_count >= cls.DAILY_LIMIT:

            return (
                False,
                'تعداد درخواست بیش از حد مجاز است'
            )

        return True, None

    # =========================
    # SEND OTP
    # =========================

    @classmethod
    def send_otp(cls, phone):

        # حذف OTPهای قبلی
        cls.objects.filter(
            phone=phone,
            is_used=False
        ).update(is_used=True)

        raw_code = cls.generate_code()

        hashed_code = make_password(raw_code)

        otp = cls.objects.create(
            phone=phone,
            code=hashed_code
        )

        from .utils import send_sms

        send_sms(
            phone,
            f'کد تایید شما: {raw_code}'
        )

        print(raw_code)

        return otp






class Header_top(models.Model):
    header_state = (
        ('active', _('active')),
        ('repose', _('repose')),
    )
    title=models.CharField(max_length=150,default="موضوع هدر سایت")
    image=models.ImageField(
        upload_to='header_images/',
        verbose_name=_('image'),
        default='default.png'
    )
    state=models.CharField(max_length=6,choices=header_state,default='repose')

    def __str__(self):
        return f"{self.title}"
    


class CustomUser(AbstractUser):
    nat_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_('nat_code'),
        validators=[
            MinLengthValidator(10, _('nat_code_must_be_10_digits')),
            MaxLengthValidator(10, _('nat_code_must_be_10_digits'))
        ]
    )
    birth_date = jmodels.jDateField(
        blank=True, 
        null=True, 
        verbose_name=_('birth_date'))
    

    favorite_products=models.ManyToManyField(Product,related_name='users_by_favorite',verbose_name=_('favorite_products'))
    is_phone_verified = models.BooleanField(default=False)
    def get_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def birth_date_shamsi(self):
        """تبدیل تاریخ میلادی به شمسی برای نمایش در فرم"""
        if self.birth_date:
            try:
                return jdatetime.date.fromgregorian(date=self.birth_date).strftime('%Y/%m/%d')
            except:
                return ''
        return ''


class SliderImage(models.Model):
    desktop_image=models.ImageField(
         upload_to='slider_image/desktop/',
        verbose_name=_('image'),
        null=True,
        blank=True
    )
    mobile_image=models.ImageField(
         upload_to='slider_image/mobile/',
        verbose_name=_('image'),
        null=True,
        blank=True
    )
    title=models.CharField(max_length=300)
    created=models.DateTimeField(auto_now=True)
    
    category_main=models.ForeignKey(CategoryMain,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=300)

    writer = models.CharField(max_length=300)

    description = models.TextField()

    intro = models.TextField(
        null=True,
        blank=True
    )

    footer = models.TextField(
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='blog_image/',
        null=True,
        blank=True
    )

    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True
    )

    views = models.PositiveIntegerField(
        default=0
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(
                self.title,
                allow_unicode=True
            )

            original_slug = self.slug
            counter = 1

            while Blog.objects.filter(
                slug=self.slug
            ).exclude(
                pk=self.pk
            ).exists():

                self.slug = (
                    f"{original_slug}-{counter}"
                )

                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class OrderBasket(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_basket')
    color=models.ForeignKey(ColorProduct,on_delete=models.CASCADE,related_name='order_basket',null=True,blank=True)
    body_color=models.ForeignKey(ColorProduct,on_delete=models.SET_NULL,null=True,related_name="orderbasket_body")
    door_color=models.ForeignKey(ColorProduct,on_delete=models.SET_NULL,null=True,related_name="orderbasket_door")
    number=models.PositiveSmallIntegerField()
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='order_basket')
    

    # def __str__(self):
    #     return f"{self.prodcut.name},{self.user},{self.color},{self.number}"


class AdItem(models.Model):
    image=models.ImageField(
         upload_to='AdSection_image/',
         verbose_name=_('image'),
     )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

   
class AdSection(models.Model):
    ad_state = (
         ('active', _('active')),
         ('repose', _('repose')),
     )
    title=models.CharField(max_length=300,null=True,blank=True)
    image=models.ManyToManyField(AdItem)
    category_main=models.ForeignKey(CategoryMain,on_delete=models.CASCADE)
    state=models.CharField(max_length=6,choices=ad_state,default='repose')

import secrets
from django.utils import timezone

def generate_discount_code(length=10):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


class DiscountCode(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name='کد تخفیف'
    )

    percent_off = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        verbose_name='درصد تخفیف'
    )

    max_discount_amount = models.PositiveIntegerField(
        verbose_name='حداکثر مبلغ تخفیف'
    )

    min_order_amount = models.PositiveIntegerField(
        default=0,
        verbose_name='حداقل مبلغ سفارش'
    )

    usage_limit = models.PositiveIntegerField(
        default=1,
        verbose_name='حداکثر تعداد استفاده'
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='used_discount_codes',
        verbose_name='کاربران استفاده کننده'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )

    start_date = jmodels.jDateTimeField(
        null=True,
        blank=True,
        verbose_name='تاریخ شروع'
    )

    expire_date = jmodels.jDateTimeField(
        null=True,
        blank=True,
        verbose_name='تاریخ انقضا'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.code:
            while True:
                code = generate_discount_code()
                if not DiscountCode.objects.filter(code=code).exists():
                    self.code = code
                    break

        super().save(*args, **kwargs)

    @property
    def used_count(self):
        return self.users.count()

    @property
    def is_valid(self):
        now = timezone.now()

        if not self.is_active:
            return False

        if self.start_date and now < self.start_date:
            return False

        if self.expire_date and now > self.expire_date:
            return False

        if self.used_count >= self.usage_limit:
            return False

        return True

    def user_can_use(self, user):
        if not self.is_valid:
            return False

        if self.users.filter(pk=user.pk).exists():
            return False

        return True

    def __str__(self):
        return f"{self.code} ({self.percent_off}%)"


