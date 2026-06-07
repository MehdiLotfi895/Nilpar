from django.contrib import admin
from .models import Product , Question , Answer  , Comment ,Feature ,Image_profile_product , Order ,AddressInfo ,HandOverOrder ,CustomUser ,ColorProduct,Header_top,CategoryMain,CategorySecondary,SliderImage,Blog,OrderBasket,AdItem ,AdSection
from django_jalali.admin.filters import JDateFieldListFilter
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from iranian_cities.admin import IranianCitiesAdmin

admin.site.register(AdItem)
admin.site.register(AdSection)
admin.site.register(CategoryMain)
admin.site.register(CategorySecondary)
admin.site.register(SliderImage)
admin.site.register(Blog)
admin.site.register(OrderBasket)
@admin.register(AddressInfo)
class AddressInfoAdmin(IranianCitiesAdmin):
    list_display = ['user', 'province', 'city', 'address']
class CategorySecond(admin.StackedInline):
    model=CategorySecondary
    extra=0
    
class ImageProfileProductInline(admin.StackedInline):
    model=Image_profile_product
    extra=0

class QuestionInline(admin.StackedInline):
    model=Question
    extra=0
class CommentInline(admin.StackedInline):
    model=Comment
    extra=0

class AnswerInline(admin.StackedInline):
    model=Answer
    extra=1
admin.site.register(ColorProduct)


class ProductPriceAdminFilter(admin.SimpleListFilter):
    title=_('price')
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('0=<price<3', _('lest_than_3')),
            ('3=<price<10', _('between_3_10')),
            ('more_than_10',_('more_than_10'))
        )
    
    def queryset(self, request, queryset):
        if self.value() == '0=<price<3':
            return queryset.filter(price__lt=3000000)
        if self.value() == '3=<price<10':
            return queryset.filter(price__gte=3000000,price__lt=10000000)
        if self.value() == 'more_than_10':
            return queryset.filter(price__lte=10000000)
        return queryset
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'old_price', 'stock', 'created_at','off')
    exclude = ('slug',)   
    inlines = [ImageProfileProductInline, QuestionInline, CommentInline]
    search_fields = ('name', 'slug','old_price',)
    list_filter=(ProductPriceAdminFilter,'stock')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=('admin_answer','description','question','created_at')
    list_per_page=20


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=('user','description','product','state')
    list_editable=('state',)
    inlines=(AnswerInline,)
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('user','state','description','product','created_at')
    list_editable=('state',)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display=('created','title','description')
    list_editable=('title','description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('user','date','clock','state','created_at')


# admin.site.register(OrderBasket)

class AddressInfoInline(admin.StackedInline):
    model=AddressInfo
    extra=0

@admin.register(HandOverOrder)
class HandOverOrderAdmin(admin.ModelAdmin):
    list_display=('date','clock','order')
    list_filter = (
        ('date', JDateFieldListFilter),
    )



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
   inlines=(AddressInfoInline,)
   fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("MoreInfo"), {"fields": ("nat_code", "birth_date","favorite_products","is_phone_verified",)}),
    )
   add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2","first_name","last_name","email","is_phone_verified",),
            },
        ),
    )
   
@admin.register(Header_top)
class HeaderTopAdmin(admin.ModelAdmin):
    list_display=('title','state')
    list_editable=('state',)