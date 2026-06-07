# main/context_processors.py

from .models import Header_top,CategoryMain


def global_data(request):
    return {
        'header_content': Header_top.objects.filter(state='active').first(),
        'main_category': CategoryMain.objects.prefetch_related(
            'secondary_category'
        ).all().order_by('-id')
    }