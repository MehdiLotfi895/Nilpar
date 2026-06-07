# utils.py
from kavenegar import *
from django.conf import settings

def send_sms(phone, message):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        
        params = {
            'sender': settings.KAVENEGAR_SENDER,
            'receptor': phone,
            'message': message
        }
        
        api.sms_send(params)
        return True
    
    except APIException as e:
        print(f"خطای کاوه‌نگار: {e}")
        return False
    
    except Exception as e:
        print(f"خطای عمومی: {e}")
        return False



# utils.py

from django.conf import settings


def send_order_customer_sms(order):

    message = f"""
سفارش شما با موفقیت ثبت شد.

کد سفارش: {order.id}
کد رهگیری: {order.tracking_code}

مبلغ سفارش:
{order.total_price:,} تومان

صنایع چوبی نیلپر
"""

    return send_sms(
        order.phonenumber,
        message
    )


def send_order_admin_sms(order):

    message = f"""
سفارش جدید ثبت شد

شماره سفارش:
{order.id}

کد رهگیری:
{order.tracking_code}

نام گیرنده:
{order.receiver}

موبایل:
{order.phonenumber}

استان:
{order.province}

شهر:
{order.city}

مبلغ:
{order.total_price:,} تومان

وضعیت:
{order.state}
"""

    return send_sms(
        settings.ADMIN_PHONE,
        message
    )