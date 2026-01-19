from .models import Category, District
from spotapp_admin.models import Osirase

def common_nav_data(request):
    return {
        "categories": Category.objects.all(),
        "districts": District.objects.all(),
        "osirase_list": Osirase.objects.all(),
    }
