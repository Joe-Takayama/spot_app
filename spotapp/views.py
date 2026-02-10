from django.db.models import Avg, Prefetch, Exists, OuterRef

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .forms import (
    ProfileEditForm,
    PasswordChangeOnlyForm,
    SignupForm,
    ContactForm,
    LoginForm,

)

from .models import Events, Review, Spot , Profile, Favorite, Category, District, OsiraseRead
from spotapp_admin.models import Photo, Osirase

from django.contrib.auth import get_user_model
User = get_user_model()

from django.http import HttpResponseForbidden

from django.urls import reverse

# ------------------------
# インデックス
# ------------------------
# ------------------------
# インデックス
# ------------------------
class IndexView(View):
    def get(self, request):
        slide_photos = (
            Photo.objects
            .select_related('spot')
            .filter(spot__isnull=False)
            .order_by('-uploaded_at')
        )

        return render(request, 'spotapp/index.html', {'slide_photos': slide_photos})


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
    login_url = "spotapp:login"
    def get(self, request):
        form = ProfileEditForm(instance=request.user, user=request.user)
        return render(request, "spotapp/profile_edit.html", {"form": form})

    def post(self, request):
        user = request.user
        form = ProfileEditForm(request.POST or None, instance=request.user, user=request.user)

        icon_file = request.FILES.get('icon')

         # まずバリデーション（重複チェックもここで走る）
        if not form.is_valid():
            return render(request, "spotapp/profile_edit.html", {"form": form})
        
         # ② 「変更なし」を弾く（username変更なし & icon未選択）
        if (not form.has_changed()) and (not icon_file):
            form.add_error(None, "変更内容がありません。")
            return render(request, "spotapp/profile_edit.html", {"form": form})

        # ③ username変更があった時だけ保存（無駄更新しない）
        if form.has_changed():
            form.save()

        
        # profile が無い場合も作る（保険）
        profile, _ = Profile.objects.get_or_create(user=user)

        if icon_file:
            profile.icon = icon_file
            profile.save()

        return redirect("spotapp:profile_edit_complete")



class ProfileEditCompleteView(LoginRequiredMixin, View):
    login_url = "spotapp:login"
    def get(self, request):
        return render(request, "spotapp/profile_edit_complete.html")


# ------------------------
# パスワード変更
# ------------------------
class PasswordChangeView(LoginRequiredMixin, View):
    login_url = "spotapp:login"
    def get(self, request):
        form = PasswordChangeOnlyForm(request.user)
        return render(request, "spotapp/password_change.html", {"form": form})

    def post(self, request):
        form = PasswordChangeOnlyForm(request.user, request.POST)

        if not form.is_valid():
            return render(request, "spotapp/password_change.html", {"form": form})

        request.user.set_password(form.cleaned_data["new_password1"])
        request.user.save()
        update_session_auth_hash(request, request.user)

        return redirect("spotapp:password_change_complete")


class PasswordChangeCompleteView(LoginRequiredMixin, View):
    login_url = "spotapp:login"
    def get(self, request):
        return render(request, "spotapp/password_change_complete.html")


# ------------------------
# 観光地検索結果
# ------------------------
class SpotSearchResultView(View):
    def get(self, request):
        keyword = request.GET.get('q', '').strip()

        category_id = request.GET.get('category', '').strip()
        district_id = request.GET.get('district', '').strip()

        spots = (
            Spot.objects
            .annotate(avg_rating=Avg('review__rating'))
            .prefetch_related(
                Prefetch('spot_photos', queryset=Photo.objects.order_by('uploaded_at'))
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
        
        # カテゴリ絞り込み
        if category_id:
            spots = spots.filter(category_id=category_id)

        # 地区絞り込み
        if district_id:
            spots = spots.filter(district_id=district_id)

            # ▼ ボタン表記用の「名前」を作る
        selected_category_name = "カテゴリ"
        selected_district_name = "地区別"

        # 絞り込みはその後
        if category_id:
            spots = spots.filter(category_id=category_id)
        if district_id:
            spots = spots.filter(district_id=district_id)

        if category_id:
            c = Category.objects.filter(category_id=category_id).first()
            if c:
                selected_category_name = c.category_name

        if district_id:
            d = District.objects.filter(district_id=district_id).first()
            if d:
                selected_district_name = d.district_name



        return render(request, 'spotapp/spot_searchresult.html', {
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


# ------------------------
# 観光地詳細
# ------------------------
class SpotDetailView(View):
    def get(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)

        is_favorited = False
        if request.user.is_authenticated:
            is_favorited = Favorite.objects.filter(user=request.user, spot=spot).exists()

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
    login_url = "spotapp:login"
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

        return redirect(
            reverse('spotapp:review_complete', kwargs={'spot_id': spot.spot_id})
        )


class ReviewCompleteView(LoginRequiredMixin, View):
    login_url = "spotapp:login"
    def get(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)
        return render(
            request,
            "spotapp/review_complete.html",
            {"spot": spot}
        )


class ReviewDetailView(View):
    def get(self, request, spot_id):
        spot = get_object_or_404(Spot, spot_id=spot_id)

        show_all = request.GET.get("all") == "1"

        qs = spot.review_set.order_by("-posted_at")
        total = qs.count()

        reviews = qs if show_all else qs[:2]
        has_more = (not show_all) and (total > 2)

        return render(request, "spotapp/review_detail.html", {
            "spot": spot,
            "reviews": reviews,
            "has_more": has_more,
            "show_all": show_all,
            "total_reviews": total,
        })



#レビュー消去用
@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, review_id=review_id)


    if review.user != request.user:
        return HttpResponseForbidden("削除権限がありません")

    if request.method == "POST":
        spot_id = review.spot.spot_id
        review.delete()
        return redirect('spotapp:review_detail', spot_id=spot_id)
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
# イベント用にういいいいいいいいい
# ------------------------
class EventListView(View):
    def get(self, request):
        month = request.GET.get("month")  # ← 追加
        page_number = request.GET.get("page", 1)

        event_list = Events.objects.order_by("event_start")

        # 🔹 月指定があれば絞り込み
        if month:
            event_list = event_list.filter(event_start__month=month)

        # ページネーション
        paginator = Paginator(event_list, 7)
        page_obj = paginator.get_page(page_number)

        context = {
            "event_list": page_obj,
            "page_obj": page_obj,
            "months": range(1, 13),
            "selected_month": month,  # ← 追加
        }

        return render(request, "spotapp/event_chart.html", context)



class EventDetailView(View):
    def get(self, request, event_id):
        event = get_object_or_404(Events, event_id=event_id)

        # 紐づいている観光地（あれば）
        spot = event.spot_id  # ForeignKey の名前が spot_id だからこれでOK

        # 評価用（お好みだけど、あると便利）
        avg_rating = None
        review_count = 0
        if spot is not None:
            reviews = Review.objects.filter(spot=spot)
            review_count = reviews.count()
            avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"]

        context = {
            "event": event,
            "spot": spot,
            "avg_rating": avg_rating,
            "review_count": review_count,
        }
        return render(request, "spotapp/event_detail.html", context)


# ------------------------
# お問い合わせ
# ------------------------
class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "spotapp/contact.html", {"form": form})

    @staticmethod
    def send_mail_from_account(subject, body):
        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                #↓ここにメールを増やせば受け取れる人が増える
                to=["mit2471573@stu.o-hara.ac.jp"], 
            )
            email.send()
        except Exception as e:
            print("メール送信失敗: ", e)
            
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


# お知らせ詳細
class NewsDetailView(View):
    def get(self, request, pk):
        news = get_object_or_404(Osirase, pk=pk)

        if request.user.is_authenticated:
            OsiraseRead.objects.get_or_create(user=request.user, osirase=news)
        else:
            read_ids = set(request.session.get("osirase_read_ids", []))
            read_ids.add(news.pk)
            request.session["osirase_read_ids"] = list(read_ids)
            request.session.modified = True

        return render(request, "spotapp/news_detail.html", {"news": news})
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
