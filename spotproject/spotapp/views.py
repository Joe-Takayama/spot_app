from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from .forms import ContactForm


from .forms import ProfileEditForm, PasswordChangeOnlyForm, SignupForm, ContactForm

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
            user = form.save(commit=False)   # まず user インスタンス作成（DB にはまだ保存しない）
            user.set_password(form.cleaned_data["password"])  # パスワードをハッシュ化
            user.save()  # ← DB に保存！（ここが本物の save）

            login(request, user)  # 自動ログイン
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
        user = request.user
        form = ProfileEditForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            # アイコンファイルが送信されていたら Profile に保存
            icon_file = request.FILES.get('icon')
            try:
                profile = user.profile
            except Exception:
                # もし Profile がなければ作成
                from .models import Profile
                profile = Profile.objects.create(user=user)

            if icon_file:
                profile.icon = icon_file
                profile.save()

            return redirect("spotapp:profile_edit_complete")

        return render(request, "spotapp/profile_edit.html", {"form": form})


# プロフィール編集完了ビュー
class ProfileEditCompleteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "spotapp/profile_edit_complete.html")


#パスワード変更ビュー
class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeOnlyForm()
        return render(request, "spotapp/password_change.html", {"form": form})

    def post(self, request):
        user = request.user
        form = PasswordChangeOnlyForm(request.POST)

        if form.is_valid():
            p1 = form.cleaned_data["new_password1"]
            p2 = form.cleaned_data["new_password2"]

            if p1 != p2:
                return render(request, "spotapp/password_change.html",
                              {"form": form, "error": "パスワードが一致しません"})

            # 変更処理
            user.set_password(p1)
            user.save()
            update_session_auth_hash(request, user)

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
        # データベース接続したらここにお気に入り取得を書く
        favorite_list = []
        return render(request, 'spotapp/favorite_list.html',
                      {"favorites": favorite_list})
    

# イベント一覧ビュー
class EventChartView(View):
    def get(self, request):
        return render(request, 'spotapp/event_chart.html')


# イベント詳細ビュー
class EventDetailView(View):
    def get(self, request):
        return render(request, 'spotapp/event_detail.html')

#お問い合わせビュー
from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContactForm

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "spotapp/contact.html", {"form": form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            recipient = "igakouga2n2n@gmail.com"

            send_mail(
                subject=f"お問い合わせ: {name}",
                message=f"送信者: {name}\nメール: {email}\n\n内容:\n{message}",
                from_email="no-reply@example.com",  # サーバー側の送信元
                recipient_list=[recipient],
            )
            return redirect("spotapp:contact_complete")  # 成功ページへリダイレクト

        # バリデーションエラー時は再表示
        return render(request, "spotapp/contact.html", {"form": form})
    
# お問い合わせ完了ビュー
class ContactCompleteView(View):
    def get(self,request):
        return render(request,"spotapp/contact_complete.html")

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
event_detail = EventDetailView.as_view()

contact_complete = ContactCompleteView.as_view()
