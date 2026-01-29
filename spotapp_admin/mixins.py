from django.shortcuts import redirect
from django.contrib import messages

class StaffLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if 'staff_id' not in request.session:
            messages.error(request, "ログインしてください")
            return redirect('spotapp_admin:login')
        return super().dispatch(request, *args, **kwargs)
