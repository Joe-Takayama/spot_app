from .models import Osirase

def osirase_context(request):
    return {
        "osirase_list": Osirase.objects.all().order_by('-created_at')
    }