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

class CustomUser(AbstractUser):
    nat_code=models.CharField(max_length=10,blank=True,null=True,unique=True,verbose_name=_('nate_code'),
    validators=[
       MinLengthValidator(10,'کد ملی باید ده رقمی باشد'),
       MaxLengthValidator(10,'کد ملی باید ده رقمی باشد')
    ])
    birth_date=models.DateField(blank=True,null=True,verbose_name=_('birth_date'))


    def get_name(self):
        return "%s %s %(self.first-name,self.last_name)"
    



class Feature(models.Model):
    title=models.CharField(max_length=300,verbose_name=_('title'))
    description=models.CharField(max_length=300 ,verbose_name=_('description'))
    created=jmodels.jDateTimeField(auto_now_add=True ,verbose_name=_('created'))

    def __str__(self):
        return f"{self.title},{self.description}"
    
class Category(models.Model):
    title=models.CharField(max_length=300)
    created=jmodels.jDateField(auto_now_add=True)
    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    name=models.CharField(max_length=300 ,verbose_name="نام کابینت")
    introduction=models.TextField(verbose_name="معرفی")
    features=models.ManyToManyField(Feature,blank=True,related_name='products',verbose_name="ویژگی")
    weight=models.PositiveSmallIntegerField(verbose_name="وزن")
    dimensions=models.CharField(max_length=150,verbose_name="ابعاد")
    category=models.ManyToManyField(Category,blank=True,related_name='products',verbose_name="نوع کابینت")
    more_details=models.TextField(verbose_name="جزعیات بیشتر")
    price=models.PositiveBigIntegerField(verbose_name="قیمت")
    stock=models.PositiveSmallIntegerField(verbose_name="تعداد موجودی")
    wood_kind=models.CharField(max_length=300,default='MDF',verbose_name='نوع چوب')
    created_at=jmodels.jDateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت")
    updated_at=jmodels.jDateTimeField(auto_now=True,verbose_name="تاریخ ویرایش")

    def __str__(self):
        return f"نام کالا : {self.name}  , موجودی: {self.stock} , قیمت: {self.price}"
class Comment(models.Model):
   comment_state=(
        ('c','تایید'),
        ('p','در حال پردازش'),
        ('r','رد'),
    )
   user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
   description=models.TextField()
   product=models.ForeignKey(Product,on_delete=models.CASCADE)
   state=models.CharField(max_length=1,choices=comment_state,default='p')
   created_at = jmodels.jDateTimeField(auto_now_add=True)

   def __str__(self):
       return f"کالا:{self.product},کابر:{self.user}"
class Question(models.Model):
    question_state=(
        ('c','تایید'),
        ('p','در حال پردازش'),
        ('r','رد'),
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    description=models.TextField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    state=models.CharField(max_length=1,choices=question_state,default='p')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    

    def __str__(self):
       return f" کابر : {self.user} , پست: {self.description}"
    
class Answer(models.Model):
    admin_answer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    description=models.TextField()
    question=models.OneToOneField(Question,on_delete=models.CASCADE)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at=jmodels.jDateField(auto_now=True,verbose_name="تاریخ ویرایش")
    def __str__(self):
       return f"توضیحات:{self.description},کابر:{self.question}"   


class Image_profile_product(models.Model):
    image=models.ImageField(upload_to='products_image/',verbose_name="عکس کابینت")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')


    def __str__(self):
        return f"{self.product}"






class AddressInfo(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='address')
    address=models.TextField(blank=True,null=True)
    address_code=models.CharField(max_length=10,null=True,blank=True)
    phonenumber=models.CharField(max_length=11)
    receiver=models.CharField(max_length=300)
    updated_at=jmodels.jDateTimeField(auto_now=True,verbose_name="تاریخ ویرایش")
    created_at=jmodels.jDateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت سفارش")
    def __str__(self):
        return f"{self.user} , {self.address}"
    


class Order(models.Model):
    order_state=(
        ('payed','پرداخت کرده'),
        ('paying','در حال پرداخت'),
        ('unpay','پرداخت نکرد'),
    )
    products=models.ManyToManyField(Product,verbose_name="نام سفارسش ها")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="کابر")
    address=models.TextField(blank=True,null=True,verbose_name="آدرس")
    address_code=models.CharField(max_length=10,null=True,blank=True,verbose_name="کدپستی")
    phonenumber=models.CharField(max_length=11,verbose_name="تلفن همراه")
    receiver=models.CharField(max_length=300,verbose_name="نام دریافت کننده")
    date=jmodels.jDateField(verbose_name="تاریخ ارسال کالا")
    clock=models.CharField(max_length=300,verbose_name="ساعت ارسال ")
    created_at=jmodels.jDateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت سفارش")
    total_price=models.PositiveIntegerField(verbose_name="قیمت کل سفارش")
    updated_at=jmodels.jDateTimeField(auto_now=True,verbose_name="تاریخ ویرایش")
    state=models.CharField(max_length=6,choices=order_state,default='paying')

    authority=models.CharField(max_length=200,blank=True,null=True)
    ref_id=models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return f"{self.products} , {self.user} , {self.created_at}"


class OrderBasket(models.Model):
    products=models.ManyToManyField(Product,verbose_name="نام سفارش ها")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="کابر",related_name='orderbasket')
    created_at=jmodels.jDateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت سفارش")
    updated_at=jmodels.jDateTimeField(auto_now=True,verbose_name="تاریخ ویرایش")
    def __str__(self):
        return f"{self.user}"
    


    

class HandOverOrder(models.Model):
    date=jmodels.jDateField()
    clock=models.CharField(max_length=300)
    order=models.OneToOneField(Order,on_delete=models.CASCADE,null=True,blank=True)
    price=models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date} , {self.clock} , {self.order}"
    
# اضافه کردن به انتهای models.py


class OTP(models.Model):
    """مدل کد یکبار مصرف"""
    phone = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)  # ← اینو عوض کن
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def is_valid(self):
        """بررسی اعتبار کد - ۵ دقیقه"""
        from django.utils import timezone
        from datetime import timedelta
        expiry_time = self.created_at + timedelta(minutes=5)
        return timezone.now() < expiry_time and not self.is_used
    
    @staticmethod
    def generate_code():
        """تولید کد ۶ رقمی"""
        import random
        import string
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def send_otp(phone):
        """ارسال کد OTP"""
        code = OTP.generate_code()
        otp = OTP.objects.create(phone=phone, code=code)
        
        from .utils import send_sms
        send_sms(phone, f'کد تأیید شما: {code}')
        
        return otp
    
    def __str__(self):
        return f"{self.phone} - {self.code}"


    