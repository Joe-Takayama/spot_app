from datetime import timedelta
from django.utils import timezone
from .models import Category, District
from spotapp_admin.models import Osirase
from .models import OsiraseRead

def common_nav_data(request):
    return {
        "categories": Category.objects.all(),
        "districts": District.objects.all(),
    }

def osirase_common(request):
    since = timezone.now() - timedelta(days=7)

    # ドロップダウン表示用（最新10件）
    osirase_list = Osirase.objects.order_by("-created_at")[:10]

    if request.user.is_authenticated:
        read_ids = set(
            OsiraseRead.objects.filter(user=request.user)
            .values_list("osirase_id", flat=True)
        )
        # NEW数（直近7日 & 未読）
        new_count = (
            Osirase.objects.filter(created_at__gte=since)
            .exclude(pk__in=read_ids)
            .count()
        )
    else:
        read_ids = set(request.session.get("osirase_read_ids", []))
        new_count = (
            Osirase.objects.filter(created_at__gte=since)
            .exclude(pk__in=read_ids)
            .count()
        )

    return {
        "osirase_list": osirase_list,
        "osirase_new_count": new_count,  # ← テンプレはこれを使う
    }