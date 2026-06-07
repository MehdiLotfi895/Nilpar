# app/templatetags/jalali_fa.py
from django import template
import jdatetime

register = template.Library()

@register.filter
def persian_weekday(date):
    """تبدیل نام روزهای هفته به فارسی"""
    if not date:
        return ""
    
    # تبدیل به تاریخ جلالی
    try:
        if isinstance(date, jdatetime.datetime):
            jalali_date = date
        else:
            # اگر تاریخ Django یا Python باشه
            jalali_date = jdatetime.datetime.fromgregorian(datetime=date)
    except:
        # اگر رشته باشه یا مشکل داشت
        return str(date)
    
    # روزهای هفته فارسی
    weekdays = [
        'شنبه',      # 0
        'یکشنبه',    # 1  
        'دوشنبه',    # 2
        'سه‌شنبه',   # 3
        'چهارشنبه',  # 4
        'پنجشنبه',   # 5
        'جمعه'       # 6
    ]
    
    return weekdays[jalali_date.weekday()]

@register.filter
def persian_date(date, format_str="%Y/%m/%d"):
    """نمایش تاریخ فارسی"""
    if not date:
        return ""
    
    try:
        if isinstance(date, jdatetime.datetime):
            jalali_date = date
        else:
            jalali_date = jdatetime.datetime.fromgregorian(datetime=date)
        
        # روز هفته فارسی
        weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
        weekday_fa = weekdays[jalali_date.weekday()]
        
        # ماه‌های فارسی
        months = {
            'Farvardin': 'فروردین',
            'Ordibehesht': 'اردیبهشت',
            'Khordad': 'خرداد',
            'Tir': 'تیر',
            'Mordad': 'مرداد',
            'Shahrivar': 'شهریور',
            'Mehr': 'مهر',
            'Aban': 'آبان',
            'Azar': 'آذر',
            'Dey': 'دی',
            'Bahman': 'بهمن',
            'Esfand': 'اسفند'
        }
        
        # فرمت کردن تاریخ
        formatted = jalali_date.strftime(format_str)
        
        # جایگزینی ماه‌های انگلیسی با فارسی
        for eng, fa in months.items():
            formatted = formatted.replace(eng, fa)
        
        return formatted
        
    except Exception as e:
        return str(date)

@register.filter
def full_persian_date(date):
    """تاریخ کامل فارسی: چهارشنبه ۱۴۰۲/۱۰/۲۷"""
    if not date:
        return ""
    
    try:
        if isinstance(date, jdatetime.datetime):
            jalali_date = date
        else:
            jalali_date = jdatetime.datetime.fromgregorian(datetime=date)
        
        weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
        weekday_fa = weekdays[jalali_date.weekday()]
        
        return f"{weekday_fa} {jalali_date.strftime('%Y/%m/%d')}"
        
    except:
        return str(date)

@register.filter
def smart_persian_date(date, format_str=None):
    """فیلتر هوشمند که هم با jdate کار کنه هم مستقل"""
    if not date:
        return ""
    
    try:
        # اول سعی کن از jdate اصلی استفاده کنی
        try:
            from django_jalali.templatetags.jformat import jdate
            result = jdate(date, format_str or "%A %Y/%m/%d")
        except:
            # اگر jdate نبود، خودمون تبدیل کنیم
            if isinstance(date, jdatetime.datetime):
                jalali_date = date
            else:
                jalali_date = jdatetime.datetime.fromgregorian(datetime=date)
            
            result = jalali_date.strftime(format_str or "%A %Y/%m/%d")
        
        # تبدیل روزهای هفته
        weekdays_map = {
            'Saturday': 'شنبه',
            'Sunday': 'یکشنبه', 
            'Monday': 'دوشنبه',
            'Tuesday': 'سه‌شنبه',
            'Wednesday': 'چهارشنبه',
            'Thursday': 'پنجشنبه',
            'Friday': 'جمعه'
        }
        
        for eng, fa in weekdays_map.items():
            result = result.replace(eng, fa)
        
        return result
        
    except Exception as e:
        return str(date)

