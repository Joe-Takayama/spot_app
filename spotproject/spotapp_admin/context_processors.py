from datetime import timedelta
from django.utils import timezone
from .models import Osirase, Staff


def osirase_nav(request):
    now = timezone.now()
    new_threshold = now - timedelta(days=7)

    items = Osirase.objects.order_by('-created_at')

    staff = None
    staff_id = request.session.get('staff_id')
    if staff_id:
        try:
            staff = Staff.objects.get(staff_id=staff_id)
        except Staff.DoesNotExist:
            pass

    new_count = 0
    for o in items:
        o.is_new = (
            o.created_at >= new_threshold and
            (staff not in o.read_by.all() if staff else True)
        )

        print(
            "TITLE:", o.title,
            "| created_at:", o.created_at,
            "| threshold:", new_threshold,
            "| staff:", staff,
            "| read_by:", list(o.read_by.all()),
            "| is_new:", o.is_new
        )
        if o.is_new:
            new_count += 1

    return {
        "osirase_list": items,
        "new_count": new_count,
    }
