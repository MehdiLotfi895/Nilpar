# errors.py
from django.shortcuts import render


def error_403(request, exception):
    return render(request, 'errors/error.html', {
        'status_code': 403,
        'title': 'دسترسی غیرمجاز',
        'message': 'متأسفانه شما اجازه دسترسی به این صفحه را ندارید.',
        'icon': 'fa-user-lock',
        'bg_color': '#fff3cd'
    }, status=403)


def error_404(request, exception):
    return render(request, 'errors/error.html', {
        'status_code': 404,
        'title': 'صفحه پیدا نشد',
        'message': 'صفحه‌ای که به دنبال آن هستید وجود ندارد یا منتقل شده است.',
        'icon': 'fa-search',
        'bg_color': '#f8d7da'
    }, status=404)


def error_405(request, exception):
    return render(request, 'errors/error.html', {
        'status_code': 405,
        'title': 'متود مجاز نیست',
        'message': 'روش درخواست ارسالی برای این صفحه مجاز نیست.',
        'icon': 'fa-ban',
        'bg_color': '#fff3cd'
    }, status=405)


def error_500(request):
    return render(request, 'errors/error.html', {
        'status_code': 500,
        'title': 'خطای سرور',
        'message': 'متأسفانه مشکلی در سرور به وجود آمده است. لطفاً بعداً تلاش کنید.',
        'icon': 'fa-server',
        'bg_color': '#f8d7da'
    }, status=500)


def error_400(request, exception):
    return render(request, 'errors/error.html', {
        'status_code': 400,
        'title': 'درخواست نامعتبر',
        'message': 'درخواست ارسالی شما نامعتبر است.',
        'icon': 'fa-exclamation-triangle',
        'bg_color': '#fff3cd'
    }, status=400)