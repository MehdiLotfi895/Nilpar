# forms.py
from django import forms
from .models import AddressInfo ,CustomUser
from django_jalali.admin import jDateField
import jdatetime

class PhoneForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': 'شماره موبایل',
            'class': 'form-input',
            'required': 'required',
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره موبایل باید با 09 شروع شود')
        if len(phone) != 11 or not phone.isdigit():
            raise forms.ValidationError('شماره موبایل باید ۱۱ رقم باشد')
        return phone


class OTPForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'کد ۶ رقمی',
            'class': 'form-input',
            'required': 'required',
            'maxlength': '6',
        })
    )
    
    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError('کد باید ۶ رقم باشد')
        return code


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'نام',
            'class': 'form-input',
            'required': 'required'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'نام خانوادگی',
            'class': 'form-input',
            'required': 'required'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'ایمیل',
            'class': 'form-input',
            'required': 'required'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
from iranian_cities.models import City


class AddAddressForm(forms.ModelForm):

    class Meta:
        model = AddressInfo

        fields = [
            'city',
            'address',
            'address_code',
            'phonenumber',
            'receiver',
        ]

        widgets = {
            'city': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'id_city',
                }
            ),
            'address': forms.Textarea(
                attrs={
                    'class': 'form-textarea',
                    'placeholder': 'خیابان، کوچه، پلاک، طبقه، واحد...',
                }
            ),
            'address_code': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'maxlength': 10,
                    'placeholder': '۱۲۳۴۵۶۷۸۹۰',
                }
            ),
            'phonenumber': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'maxlength': 11,
                    'placeholder': '۰۹۱۲۳۴۵۶۷۸۹',
                }
            ),
            'receiver': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'نام و نام خانوادگی گیرنده',
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['city'].queryset = (
            City.objects
            .filter(province_id=8)
            .order_by('name')
        )

        self.fields['city'].empty_label = 'انتخاب شهر'

    def clean_city(self):

        city = self.cleaned_data['city']

        if city.province_id != 8:

            raise forms.ValidationError(
                'در حال حاضر فقط شهرهای استان تهران پشتیبانی می‌شوند.'
            )

        return city

    def clean_address_code(self):

        address_code = self.cleaned_data['address_code']

        if not address_code.isdigit():

            raise forms.ValidationError(
                'کد پستی باید فقط شامل عدد باشد.'
            )

        if len(address_code) != 10:

            raise forms.ValidationError(
                'کد پستی باید ۱۰ رقم باشد.'
            )

        return address_code

    def clean_phonenumber(self):

        phone = self.cleaned_data['phonenumber']

        if not phone.isdigit():

            raise forms.ValidationError(
                'شماره تماس باید فقط شامل عدد باشد.'
            )

        if len(phone) != 11:

            raise forms.ValidationError(
                'شماره تماس باید ۱۱ رقم باشد.'
            )

        if not phone.startswith('09'):

            raise forms.ValidationError(
                'شماره موبایل معتبر نیست.'
            )

        return phone



# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model=CustomUser
#         fields=("first_name","last_name","email","nat_code","birth_date")
    


class ProfileForm(forms.ModelForm):
    birth_date_shamsi = forms.CharField(
        required=False,
        label='تاریخ تولد',
        widget=forms.TextInput(attrs={
            'placeholder': 'مثال: 1400/11/29',
            'class': 'form-input'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'nat_code')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # مقدار اولیه شمسی رو直接从 birth_date بگیر
        if self.instance and self.instance.pk:
            if self.instance.birth_date:
                # چون birth_date خودش شمسی هست، مستقیم استفاده می‌کنیم
                try:
                    # اگر birth_date از نوع jDate است
                    shamsi_date = self.instance.birth_date
                    self.initial['birth_date_shamsi'] = str(shamsi_date).replace('-', '/')
                except:
                    self.initial['birth_date_shamsi'] = ''
            else:
                self.initial['birth_date_shamsi'] = ''
    
    def clean_birth_date_shamsi(self):
        date_str = self.cleaned_data.get('birth_date_shamsi', '').strip()
        
        # اگه خالی باشه
        if not date_str:
            self.instance.birth_date = None
            return ''
        
        try:
            # پارس کردن فرمت
            parts = date_str.replace('-', '/').split('/')
            if len(parts) != 3:
                raise ValueError()
            
            year, month, day = map(int, parts)
            
            # اعتبارسنجی
            if not (1300 <= year <= 1500):
                raise forms.ValidationError('سال باید بین 1300 تا 1500 باشد')
            if not (1 <= month <= 12):
                raise forms.ValidationError('ماه باید بین 1 تا 12 باشد')
            if not (1 <= day <= 31):
                raise forms.ValidationError('روز باید بین 1 تا 31 باشد')
            
            # اعتبارسنجی تاریخ شمسی معتبر
            try:
                jalali_date = jdatetime.date(year, month, day)
                # فقط برای اعتبارسنجی - اگر تاریخ نامعتبر باشد خطا می‌دهد
                test_date = jalali_date  # نیازی به تبدیل به میلادی نیست
            except (ValueError, jdatetime.dateError):
                raise forms.ValidationError('تاریخ شمسی نامعتبر است')
            
            # ✅ مستقیماً تاریخ شمسی رو به صورت رشته ذخیره می‌کنیم
            # برای jmodels.jDateField باید به فرمت ISO برگردونیم
            formatted_date = f"{year}-{month:02d}-{day:02d}"
            self.instance.birth_date = formatted_date
            
            # برگردون به فرمت نمایشی با اسلش
            return f"{year}/{month:02d}/{day:02d}"
            
        except (ValueError, IndexError):
            raise forms.ValidationError('تاریخ نامعتبر. فرمت صحیح: 1400/11/29')
        



class AddressUpdateForm(forms.ModelForm):

    class Meta:
        model = AddressInfo

        fields = [
            'city',
            'address',
            'address_code',
            'phonenumber',
            'receiver',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['city'].queryset = City.objects.filter(
            province_id=8
        ).order_by('name')

    def clean_city(self):

        city = self.cleaned_data['city']

        if city.province_id != 8:

            raise forms.ValidationError(
                "فقط شهرهای استان تهران مجاز هستند."
            )

        return city