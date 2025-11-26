from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import StaffForm, EventCreateForm, PhotoForm,SpotCreateForm
from .models import Staff, Events
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .mixins import StaffLoginRequiredMixin


#ホーム画面
class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp_admin/index.html')
    

#登録選択画面
class RegistselectView(StaffLoginRequiredMixin, View):
    def get(self,request):
        return render(request,'spotapp_admin/Registrationselection.html')
    

# ログイン画面
class LoginView(View):
    def get(self, request):
        form = StaffForm()
        return render(request, 'registration/login.html', {'form': form})
    
    def post(self, request):
        form = StaffForm(request.POST)

        if not form.is_valid():
            return render(request, 'registration/login.html', {'form': form})
        
        name = form.cleaned_data['name']
        password = form.cleaned_data['password']

        # 名前で検索
        try:
            staff = Staff.objects.get(name=name)
        except Staff.DoesNotExist:
            messages.error(request, '職員名が正しくありません')
            return render(request, 'registration/login.html', {'form': form})
        
        # パスワード照合
        if check_password(password, staff.password):
            # ログイン成功
            request.session['staff_id'] = str(staff.staff_id)
            return redirect('spotapp_admin:index')
        
        # パスワード不一致
        messages.error(request, 'パスワードが違います')
        return render(request, 'registration/login.html', {'form': form})

# ログアウト画面 
class LogoutView(View):
    def get(self, request):
        return render(request, 'registration/logout.html')
    
    def post(self, request):
        request.session.flush()
        return redirect('spotapp_admin:index')

#更新削除選択画面
class updelView(StaffLoginRequiredMixin, View):
    def get(self,request):
        return render(request,'spotapp_admin/updatedelete.html')



# イベント登録画面
class EventRegistrationView(StaffLoginRequiredMixin, View):
    def get(self, request):
        event_form = EventCreateForm()
        photo_form = PhotoForm()
        return render(request, 'spotapp_admin/event_registration.html', {'event_form': event_form, 'photo_form': photo_form})

    def post(self, request):
        event_form = EventCreateForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)

        if event_form.is_valid() and photo_form.is_valid():
            event = event_form.save()
            photo = photo_form.save(commit=False)
            photo.event = event
            photo.save()
            return render(request, 'spotapp_admin/event_registration_complete.html')
        return render(request, 'spotapp_admin/event_registration.html', {'event_form': event_form, 'photo_form': photo_form})
    
# イベント一覧画面
class EventListView(StaffLoginRequiredMixin, View):
    def get(self, request):
        event_list = Events.objects.order_by('-event_date')
        return render(request, 'spotapp_admin/event_update_or_delete.html', {'event_list': event_list})

# イベント更新画面  
class EventUpdateView(StaffLoginRequiredMixin, View):
    def get(self, request, event_id):
        page = get_object_or_404(Events, pk=event_id)
        event_form = EventCreateForm(instance=page)
        event_photo = PhotoForm(instance=page)
        return render(request, 'spotapp_admin/event_update.html', {'event_form': event_form, 'photo_form': event_photo, 'page': page})
    
    def post(self, request, event_id):
        page = get_object_or_404(Events, pk=event_id)
        event_form = EventCreateForm(request.POST, request.FILES, instance=page)
        photo_form = PhotoForm(request.POST, request.FILES, instance=page)

        if event_form.is_valid() and photo_form.is_valid():
            event_form.save()
            photo_form.save()
            return redirect('spotapp_admin:event_update_complete')
        return render(request, 'spotapp_admin/event_update.html', {'event_form': event_form, 'photo_form': photo_form, 'page': page})

class SpotRegistrationView(StaffLoginRequiredMixin, View):
    def get(self, request):
        spot_form = SpotCreateForm()
        photo_form = PhotoForm()
        return render(request, 'spotapp_admin/spot_registration.html', {'spot_form': spot_form, 'photo_form': photo_form})

    def post(self, request):
        spot_form = SpotCreateForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)

        if spot_form.is_valid() and photo_form.is_valid():
            spot = spot_form.save()
            photo = photo_form.save(commit=False)
            photo.spot = spot
            photo.save()
            return render(request, 'spotapp_admin/spot_registration_complete.html')
        return render(request, 'spotapp_admin/spot_registration.html', {'spot_form': spot_form, 'photo_form': photo_form})
