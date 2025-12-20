from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (
    update_session_auth_hash, authenticate, login
)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import get_connection, EmailMessage
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import (
    ProfileEditForm,
    PasswordChangeOnlyForm,
    SignupForm,
    ContactForm,
    LoginForm
)

from .models import Events, Review, Spot as UserSpot
from spotapp_admin.models import Events, Spot


# ------------------------
# インデックス
# ------------------------
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
            user = form.save()
            login(request, user)
            return redirect("spotapp:signup_complete")

        return render(request, "spotapp/signup.html", {"form": form})


class SignupCompleteView(View):
    def get(self, request):
        return render(request, 'spotapp/signup_complete.html')


# ------------------------
# プロフィール編集ビュー
# ------------------------
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileEditForm(instance=request.user)
        return render(request, "spotapp/profile_edit.html", {"form": form})

    def post(self, request):
        user = request.user
        form = ProfileEditForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            icon_file = request.FILES.get('icon')
            try:
                profile = user.profile
            except Exception:
                from .models import Profile
                profile, created = Profile.objects.get_or_create(user=user)

            if icon_file:
                profile.icon = icon_file
                profile.save()

            return redirect("spotapp:profile_edit_complete")

        return render(request, "spotapp/profile_edit.html", {"form": form})


class ProfileEditCompleteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "spotapp/profile_edit_complete.html")


# ------------------------
# パスワード変更
# ------------------------
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
                return render(
                    request,
                    "spotapp/password_change.html",
                    {"form": form, "error": "パスワードが一致しません"}
                )

            user.set_password(p1)
            user.save()
            return redirect("spotapp:password_change_complete")

        return render(request, "spotapp/password_change.html", {"form": form})


class PasswordChangeCompleteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "spotapp/password_change_complete.html")


# ------------------------
# 観光地検索結果
# ------------------------
class SpotSearchResultView(View):
    def get(self, request):
        keyword = request.GET.get('q')
        spots = Spot.objects.all()

        if keyword:
            spots = spots.filter(spot_name__icontains=keyword)

        return render(request, 'spotapp/spot_searchresult.html', {
            'keyword': keyword,
            'spots': spots,
        })


# ------------------------
# 観光地詳細
# ------------------------
class SpotDetailView(View):
    def get(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)
        return render(request, 'spotapp/spot_detail.html', {'spot': spot})

    def post(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)

        Review.objects.create(
            spot=spot,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

        return redirect('spotapp:spot_detail', spot_id=spot.spot_id)


# ------------------------
# レビュー投稿
# ------------------------
class ReviewCreateView(View):
    def get(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)
        return render(request, 'spotapp/review_create.html', {'spot': spot})

    def post(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)

        Review.objects.create(
            spot=spot,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

        return redirect('spotapp:spot_detail', spot_id=spot.spot_id)


class ReviewCompleteView(View):
    def get(self, request):
        return render(request, "spotapp/review_complete.html")


# ------------------------
# お気に入り一覧
# ------------------------
class FavoriteListView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            'spotapp/favorite_list.html',
            {"favorites": []}
        )


# ------------------------
# イベント
# ------------------------
class EventListView(View):
    def get(self, request):
        event_list = Events.objects.order_by('-event_date')
        months = range(1, 13)
        return render(request, 'spotapp/event_chart.html', {
            'event_list': event_list,
            'months': months,
        })


class EventDetailView(View):
    def get(self, request, event_id):
        event = get_object_or_404(Events, event_id=event_id)
        return render(request, 'spotapp/event_detail.html', {'event': event})


# ------------------------
# お問い合わせ
# ------------------------
class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "spotapp/contact.html", {"form": form})

    @staticmethod
    def send_mail_from_account(subject, body):
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
            from_email='igakouga2n2n@gmail.com',
            to=['mit2471573@stu.o-hara.ac.jp'],
            connection=connection,
        )
        email.send()

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            self.send_mail_from_account(
                subject=f"お問い合わせ: {name}",
                body=f"送信者: {name}\nメール: {email}\n\n内容:\n{message}"
            )

            return redirect("spotapp:contact_complete")

        return render(request, "spotapp/contact.html", {"form": form})


class ContactCompleteView(View):
    def get(self, request):
        return render(request, "spotapp/contact_complete.html")


# ------------------------
# ログイン / ログアウト
# ------------------------
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'spotapp/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, 'spotapp/login.html', {'form': form})

        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )

        if user is None:
            messages.error(request, "ユーザー名またはパスワードが違います")
            return render(request, 'spotapp/login.html', {'form': form})

        login(request, user)
        return redirect('spotapp:index')


class LogoutView(View):
    def post(self, request):
        request.session.flush()
        return redirect('spotapp:index')



        # ------------------------
        # as_view() の定義
        # ------------------------
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
event_chart = EventListView.as_view()
event_detail = EventDetailView.as_view()
contact_complete = ContactCompleteView.as_view()
