from django.db.models import Avg, Prefetch, Exists, OuterRef

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import get_connection, EmailMessage
from django.contrib import messages
from spotapp_admin.models import Osirase

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import (
    ProfileEditForm,
    PasswordChangeOnlyForm,
    SignupForm,
    ContactForm,
    LoginForm,

)

from .models import Events, Review, Spot , Profile, Favorite
from spotapp_admin.models import Photo

from django.contrib.auth import get_user_model
User = get_user_model()



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
# プロフィール表示ビュー
# ------------------------
@login_required
def profile_view(request):
    return render(request, "spotapp/profile.html")

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

        if not form.is_valid():
            return render(request, "spotapp/profile_edit.html", {"form": form})
        form.save()

        icon_file = request.FILES.get('icon')
        # profile が無い場合も作る（保険）
        profile, _ = Profile.objects.get_or_create(user=user)

        if icon_file:
            profile.icon = icon_file
            profile.save()

        return redirect("spotapp:profile_edit_complete")



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
        spots = Spot.objects.annotate(
            avg_rating=Avg('review__rating')
        ).prefetch_related(
            Prefetch(
                'spot_photos',
                queryset=Photo.objects.order_by('uploaded_at')
            )
        )
        
        if request.user.is_authenticated:
            favorites_subquery = Favorite.objects.filter(
                user=request.user,
                spot=OuterRef('pk')
            )
            spots = spots.annotate(
                is_favorited=Exists(favorites_subquery)
            )
        else:
            spots = spots.annotate(is_favorited=Exists(Favorite.objects.none()))

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

        is_favorited = False
        if request.user.is_authenticated:
            is_favorited = Favorite.objects.filter(
                user=request.user,
                spot=spot
            ).exists()

        return render(request, 'spotapp/spot_detail.html', {
            'spot': spot,
            'is_favorited': is_favorited,
        })

    def post(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)

        Review.objects.create(
            spot=spot,
            user = request.user,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

        return redirect('spotapp:spot_detail', spot_id=spot.spot_id)


# ------------------------
# レビュー投稿
# ------------------------
class ReviewCreateView(LoginRequiredMixin,View):
    def get(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)
        return render(request, 'spotapp/review_create.html', {'spot': spot})

    def post(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)

        Review.objects.create(
            user=request.user,
            spot=spot,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

        return redirect('spotapp:spot_detail', spot_id=spot.spot_id)


class ReviewCompleteView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, "spotapp/review_complete.html")

class ReviewDetailView(View):
    def get(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)

        return render(request, "spotapp/review_detail.html", {
            "spot": spot,
            "reviews": spot.review_set.all()
        })

# ------------------------
# お気に入り一覧
# ------------------------
@login_required
def favorite_list(request):
    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related("spot")
        .order_by("-created_at")
    )
    return render(request, "spotapp/favorite_list.html", {"favorites": favorites})

# ------------------------
# お気に入り追加・削除
# ------------------------
@login_required
def favorite_toggle(request, spot_id):
    if request.method != "POST":
        # GETで叩かれたら安全に戻す（最小影響）
        return redirect("spotapp:spot_detail", spot_id=spot_id)

    spot = get_object_or_404(Spot, spot_id=spot_id)

    fav, created = Favorite.objects.get_or_create(user=request.user, spot=spot)
    if created:
        messages.success(request, "お気に入りに追加したぺこ！")
    else:
        fav.delete()
        messages.info(request, "お気に入りを解除したぺこ！")

    return redirect(request.META.get("HTTP_REFERER") or "spotapp:spot_detail", spot_id=spot_id)

# ------------------------
# お気に入り追加・削除（画面遷移なし/Ajax）
# ------------------------
@login_required
@require_POST
def favorite_toggle_ajax(request, spot_id):
    spot = get_object_or_404(Spot, spot_id=spot_id)

    fav, created = Favorite.objects.get_or_create(user=request.user, spot=spot)
    if created:
        # 登録
        return JsonResponse({"ok": True, "favorited": True})
    else:
        # 解除
        fav.delete()
        return JsonResponse({"ok": True, "favorited": False})


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
            #↓ここにメールを増やせば受け取れる人が増える
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
                body=f"このメールは観光地検索システムから送信されたお問い合わせメールです\n\n送信者: {name}\nメール: {email}\n\n内容:\n{message}"
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
        Profile.objects.get_or_create(user=user)
        return redirect('spotapp:index')


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("spotapp:logout_complete")


class LogoutCompleteView(View):
    def get(self, request):
        return render(request, "spotapp/logout_complete.html")

# ------------------------
# お知らせ表示画面
def osirase_list(request):
    items = Osirase.objects.all()
    return render(request, "osirase_list.html", {"osirase_list": items})


        # ------------------------
 # as_view() の定義
# ------------------------
index = IndexView.as_view()

signup = SignupView.as_view()
signup_complete = SignupCompleteView.as_view()

login_view = LoginView.as_view()
logout_view = LogoutView.as_view()
logout_complete = LogoutCompleteView.as_view()


profile_edit = ProfileEditView.as_view()
profile_edit_complete = ProfileEditCompleteView.as_view()

password_change = PasswordChangeView.as_view()
password_change_complete = PasswordChangeCompleteView.as_view()

spot_searchresult = SpotSearchResultView.as_view()
spot_detail = SpotDetailView.as_view()

review_create = ReviewCreateView.as_view()
review_complete = ReviewCompleteView.as_view()
review_detail= ReviewDetailView.as_view()



event_chart = EventListView.as_view()
event_detail = EventDetailView.as_view()

contact_complete = ContactCompleteView.as_view()
