from .models import Category, District

def common_nav_data(request):
    return {
        "categories": Category.objects.all(),
        "districts": District.objects.all(),
    }
