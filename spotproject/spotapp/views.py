from django.shortcuts import render, redirect, get_object_or_404   # 👈 修正：get_object_or_404 追加
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileEditForm, PasswordChangeOnlyForm, SignupForm
from .models import Event   # 👈 修正：Eventモデルを使用するため追加


class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp/index.html')
    

#  新規登録ビュー   
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "spotapp/signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)  
            user.set_password(form.cleaned_data["password"])  
            user.save()
            login(request, user)  
            return redirect("spotapp:signup_complete")

        return render(request, "spotapp/signup.html", {"form": form})


# 新規登録完了ビュー
class SignupCompleteView(View):
    def get(self, request):
        return render(request, 'spotapp/signup_complete.html')


# プロフィール編集ビュー
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileEditForm(instance=request.user)
        return render(request, "spotapp/profile_edit.html", {"form": form})

    def post(self, request):
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("spotapp:profile_edit_complete")
        return render(request, "spotapp/profile_edit.html", {"form": form})


# プロフィール編集完了ビュー
class ProfileEditCompleteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "spotapp/profile_edit_complete.html")


# パスワード変更ビュー
class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeOnlyForm()
        return render(request, "spotapp/password_change.html", {"form": form})

    def post(self, request):
        form = PasswordChangeOnlyForm(request.POST)
        if form.is_valid():
            p1 = form.cleaned_data["new_password1"]
            p2 = form.cleaned_data["new_password2"]

            if p1 != p2:
                return render(request, "spotapp/password_change.html",
                              {"form": form, "error": "パスワードが一致しません"})

            request.user.set_password(p1)
            request.user.save()
            update_session_auth_hash(request, request.user)

            return redirect("spotapp:password_change_complete")

        return render(request, "spotapp/password_change.html", {"form": form})


# パスワード変更完了ビュー
class PasswordChangeCompleteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "spotapp/password_change_complete.html")


#検索結果ビュー    
class SpotSearchResultView(View):
    def get(self,request):
        return render(request, 'spotapp/spot_searchresult.html')


#観光地詳細ビュー
class SpotDetailView(View):
    def get(self,request):
        return render(request, 'spotapp/spot_detail.html')


#レビュー投稿ビュー
class ReviewCreateView(View):
    def get(self,request):
        return render(request,"spotapp/review_create.html")
    

#投稿完了ビュー
class ReviewCompleteView(View):
    def get(self,request):
        return render(request,"spotapp/review_complete.html")


# お気に入り一覧ビュー
class FavoriteListView(LoginRequiredMixin, View):
    def get(self, request):
        favorite_list = []
        return render(request, 'spotapp/favorite_list.html',
                      {"favorites": favorite_list})


#イベント一覧ビュー

class EventChartView(View):
    def get(self, request):
        events = Event.objects.all()   # 👈 修正：DBからイベント一覧を取得
        return render(request, 'spotapp/event_chart.html', {'events': events})  # 👈 修正：eventsをテンプレートに渡す


# イベント詳細ビュー 
class EventDetailView(View):
    def get(self, request, event_id):   # 👈 修正：event_id を受け取る
        event = get_object_or_404(Event, event_id=event_id)  # 👈 修正：DBから1件取得
        return render(request, 'spotapp/event_detail.html', {'event': event})  # 👈 修正：event を渡す


index = IndexView.as_view()

signup = SignupView.as_view()
signup_complete = SignupCompleteView.as_view()

profile_edit = ProfileEditView.as_view()
profile_edit_complete = ProfileEditCompleteView.as_view()

password_change = PasswordChangeView.as_view()
password_change_complete = PasswordChangeCompleteView.as_view()

spot_searchresult = SpotSearchResultView.as_view()
spot_detail = SpotDetailView.as_view()

review_create = ReviewCreateView.as_view()
review_complete = ReviewCompleteView.as_view()

favorite_list = FavoriteListView.as_view()

event_chart = EventChartView.as_view()
event_detail = EventDetailView.as_view()   # 👈 修正：そのままでOK（URL側で引数設定）
