from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash,authenticate, login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import get_connection, EmailMessage

from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import ProfileEditForm, PasswordChangeOnlyForm, SignupForm, ContactForm, LoginForm


class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp/index.html')
    
# ------------------------
# 新規登録ビュー
# ------------------------
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "spotapp/signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()  # ← パスワード暗号化は forms.py 側
            login(request, user)  # 自動ログインOK
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
                profile, created = Profile.objects.get_or_create(user=user)


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
class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "spotapp/contact.html", {"form": form})

    @staticmethod
    def send_mail_from_account(subject, body, to, from_user, password):
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='smtp.gmail.com',
            port=587,
            username='igakouga2n2n@gmail.com',
            password='ustl imeu qdcn zaql',
            use_tls=True,
        )
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_user,
            to=['mit2471573@stu.o-hara.ac.jp'],#ここにリスト型で他のメールアドレスを入れられる
            connection=connection,
        )
        email.send() 

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            recipient = "igakouga2n2n@gmail.com"

            # 複数アカウントを切り替えて送信
            self.send_mail_from_account(
                subject=f"お問い合わせ: {name}",
                body=f"送信者: {name}\nメール: {email}\n\n内容:\n{message}",
                to=[recipient],
                from_user="your_account@gmail.com",
                password="your_app_password"
            )

            return redirect("spotapp:contact_complete")

        return render(request, "spotapp/contact.html", {"form": form})
    
# お問い合わせ完了ビュー
class ContactCompleteView(View):
    def get(self,request):
        return render(request,"spotapp/contact_complete.html")

#ログインビュー
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'spotapp/login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, 'spotapp/login.html', {'form': form})

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        # Django標準の認証
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "ユーザー名またはパスワードが違います")
            return render(request, 'spotapp/login.html', {'form': form})

        login(request, user)  # ← 標準ログイン
        return redirect('spotapp:index')

# ログアウト画面 
class LogoutView(View):
    def get(self, request):
        return render(request, 'spotapp/logout.html')
    
    def post(self, request):
        request.session.flush()
        return redirect('spotapp:index')


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
