from .models import Loop

def loop_categories(request):
    return {
        'loop_categories': Loop.CATEGORY_CHOICES
    }