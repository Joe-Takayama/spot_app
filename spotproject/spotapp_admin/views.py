from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import StaffForm, EventCreateForm, PhotoForm,SpotCreateForm,OsiraseForm
from .models import Staff, Photo, Osirase
from spotapp.models import Spot, Events, Category, District
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .mixins import StaffLoginRequiredMixin
from django.db.models import Avg,Prefetch
from .utils import get_latlng
from datetime import timedelta
from django.utils import timezone


# お知らせ通知
# class OsiraseNavMixin:
#     def get_osirase_context(self, request):
#         now = timezone.now()
#         new_threshold = now - timedelta(days=3)

#         osirase_list = Osirase.objects.all().order_by('-created_at')

#         staff = None
#         staff_id = request.session.get('staff_id')
#         if staff_id:
#             try:
#                 staff = Staff.objects.get(staff_id=staff_id)
#             except Staff.DoesNotExist:
#                 pass

#         new_count = 0

#         for o in osirase_list:
#             # 3日以内 かつ 未読 の場合のみ新着
#             o.is_new = (
#                 o.created_at >= new_threshold and
#                 (staff not in o.read_by.all() if staff else True)
#             )

#             if o.is_new:
#                 new_count += 1

#         return {
#             "osirase_list": osirase_list,
#             "new_count": new_count
#         }

#ホーム画面
class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp_admin/index.html')
    

#登録選択画面
class RegistselectView(StaffLoginRequiredMixin, View):
    def get(self, request):
        return render(request,'spotapp_admin/Registrationselection.html')
    
    
#更新削除選択画面
class UpdelView(StaffLoginRequiredMixin, View):
    def get(self,request):
        return render(request,'spotapp_admin/updatedelete.html')
    
# 観光地検索結果画面
class SpotSearchView(StaffLoginRequiredMixin, View):
    def get(self, request):
        keyword = request.GET.get('q')

        category_id = request.GET.get('category', '').strip()
        district_id = request.GET.get('district', '').strip()

        spots = Spot.objects.annotate(
    avg_rating=Avg('review__rating')
).prefetch_related(
            Prefetch(
                'spot_photos',
                queryset=Photo.objects.order_by('uploaded_at')
            )
)
        if keyword:
            spots = spots.filter(spot_name__icontains=keyword)
        
        # カテゴリ絞り込み
        if category_id:
            spots = spots.filter(category_id=category_id)

        # 地区絞り込み
        if district_id:
            spots = spots.filter(district_id=district_id)

            # ▼ ボタン表記用の「名前」を作る
        selected_category_name = "カテゴリ"
        selected_district_name = "地区別"

        if category_id:
            c = Category.objects.filter(category_id=category_id).first()
            if c:
                selected_category_name = c.category_name

        if district_id:
            d = District.objects.filter(district_id=district_id).first()
            if d:
                selected_district_name = d.district_name



        return render(request, 'spotapp_admin/search-result.html', {
            'keyword': keyword,
            'spots': spots,

            # プルダウン用
            'categories': Category.objects.all(),
            'districts': District.objects.all(),

            # 選択保持
            'selected_category': category_id,
            'selected_district': district_id,

            # ボタン表記保持（追加）
            "selected_category_name": selected_category_name,
            "selected_district_name": selected_district_name,
        })


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
            return render(request, 'spotapp_admin/event_update_complete.html')
        return render(request, 'spotapp_admin/event_update.html', {'event_form': event_form, 'photo_form': photo_form, 'page': page})

# イベント削除確認画面
class EventDeleteView(StaffLoginRequiredMixin, View):
    def get(self, request, event_id):
        page = get_object_or_404(Events, pk=event_id)
        return render(request, 'spotapp_admin/event_delete.html', {'page': page})
    
    def post(self, request, event_id):
        page = get_object_or_404(Events, pk=event_id)
        event_name = page.event_name
        page.delete()
        return render(request, 'spotapp_admin/event_delete_complete.html', {'event_name': event_name})
    
# 観光地登録画面
class SpotRegistrationView(StaffLoginRequiredMixin, View):

    def get(self, request):
        spot_form = SpotCreateForm()
        photo_form = PhotoForm()
        return render(request, 'spotapp_admin/spot_registration.html', {
            'spot_form': spot_form,
            'photo_form': photo_form
        })

    def post(self, request):
        spot_form = SpotCreateForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)

        if spot_form.is_valid() and photo_form.is_valid():

            spot = spot_form.save(commit=False)

            lat, lng = get_latlng(spot.address)

            if spot.latitude is None or spot.longitude is None:
                lat, lng = get_latlng(spot.address)
                if lat is not None and lng is not None:
                    spot.latitude = lat
                    spot.longitude = lng


            spot.save()

            photo = photo_form.save(commit=False)
            photo.spot = spot
            photo.save()

            return render(request, 'spotapp_admin/spot_registration_complete.html')

        return render(request, 'spotapp_admin/spot_registration.html', {
            'spot_form': spot_form,
            'photo_form': photo_form
        })


#観光地更新画面
class SpotUpdateView(StaffLoginRequiredMixin, View):
    def get(self, request, spot_id):
        page = get_object_or_404(Spot, pk=spot_id)
        spot_form = SpotCreateForm(instance=page)
        spot_photo = PhotoForm(instance=page)
        return render(request, 'spotapp_admin/spot_update.html', {'spot_form': spot_form, 'photo_form': spot_photo, 'page': page})
    
    def post(self, request, spot_id):
        page = get_object_or_404(Spot, pk=spot_id)
        spot_form = SpotCreateForm(request.POST, request.FILES, instance=page)
        photo_form = PhotoForm(request.POST, request.FILES, instance=page)

        if spot_form.is_valid() and photo_form.is_valid():
            spot_form.save()
            photo_form.save()
            return render(request, 'spotapp_admin/spot_update_complete.html')
        return render(request, 'spotapp_admin/spot_update.html', {'spot_form': spot_form, 'photo_form': photo_form, 'page': page})
    
# 観光地削除確認画面
class SpotDeleteView(StaffLoginRequiredMixin, View):
    def get(self, request, spot_id):
        page = get_object_or_404(Spot, pk=spot_id)
        return render(request, 'spotapp_admin/spot_delete.html', {'page': page})
    
    def post(self, request, spot_id):
        page = get_object_or_404(Spot, pk=spot_id)
        spot_name = page.spot_name
        page.delete()
        return render(request, 'spotapp_admin/spot_delete_complete.html', {'spot_name': spot_name})
    
# 観光地一覧画面
class SpotListView(StaffLoginRequiredMixin, View):
    def get(self, request):
        spot_list = Spot.objects.order_by('-created_at')
        return render(request, 'spotapp_admin/spot_update_or_delete.html', {'spot_list': spot_list})

#お知らせ送信画面

class OsiraseView(StaffLoginRequiredMixin, View):
    def get(self, request):
        form = OsiraseForm()
        return render(request, 'spotapp_admin/osirase.html', {'form': form})


    def post(self, request):
        if request.method == "POST":
            form = OsiraseForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'spotapp_admin/osirase_complete.html')   # ホーム画面へ戻る
            else:
                form = OsiraseForm()
                return render(request, "spotapp_admin/osirase.html", {"form": form})


# お知らせ表示画面
def osirase_list(request):
    items = Osirase.objects.all()
    return render(request, "osirase_list.html", {"osirase_list": items})

# お知らせ詳細画面
class OsiraseDetailView(StaffLoginRequiredMixin, View):
    def get(self, request, pk):
        osirase = get_object_or_404(Osirase, pk=pk)

        staff_id = request.session.get('staff_id')
        if staff_id:
            try:
                staff = Staff.objects.get(staff_id=staff_id)
                osirase.read_by.add(staff)
            except Staff.DoesNotExist:
                pass
        return render(request, "spotapp_admin/osirase_detail.html", {"osirase": osirase})
