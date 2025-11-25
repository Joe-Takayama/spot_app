from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from django.views import View

from .forms import ProfileEditForm

class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp/index.html')
    
    
class SignupView(View):
    def signup(request):
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('spotapp:signup_complete')
        else:
            form = UserCreationForm()

        return render(request, 'spotapp/signup.html', {'form': form})

class SignupCompleteView(View):
    def get(self, request):
        return render(request, 'spotapp/signup_complete.html')
    
@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
    """プロフィール編集（ユーザー名 / パスワード変更）"""
    
    def get(self, request):
        # 今ログインしてるユーザーの情報をフォームに入れる
        form = ProfileEditForm(instance=request.user)
        return render(request, "spotapp/profile_edit.html", {"form": form})

    def post(self, request):
        user = request.user
        form = ProfileEditForm(request.POST, instance=user)

        if form.is_valid():

            # username の変更は ModelForm が処理してくれる
            user = form.save(commit=False)

            # パスワード変更がある場合
            new_password = form.cleaned_data.get("password")
            if new_password:
                user.set_password(new_password)
                user.save()
                # パスワード変更後に自動ログアウトされないための処理
                update_session_auth_hash(request, user)
            else:
                user.save()

            return redirect("spotapp:profile_edit_complete")

        # NGの場合はそのまま画面を再表示
        return render(request, "spotapp/profile_edit.html", {"form": form})


@method_decorator(login_required, name='dispatch')
class ProfileEditCompleteView(View):
    """プロフィール編集 完了画面"""
    
    def get(self, request):
        return render(request, "spotapp/profile_edit_complete.html")
    
class SpotSearchResultView(View):
    def get(self,request):
        return render(request, 'spotapp/spot_searchresult.html')
    
class SpotDetailView(View):
    def get(self,request):
        return render(request, 'spotapp/spot_detail.html')

class ReviewCreateView(View):
    def get(self,request):
        return render(request,"spotapp/review_create.html")
    
class ReviewCompleteView(View):
    def get(self,request):
        return render(request,"spotapp/review_complete.html")

index = IndexView.as_view()
signup = SignupView.signup
signup_complete = SignupCompleteView.as_view()
profile_edit = ProfileEditView.as_view()
profile_edit_complete = ProfileEditCompleteView.as_view()
spot_searchresult = SpotSearchResultView.as_view()
spot_detail = SpotDetailView.as_view()
review_create = ReviewCreateView.as_view()
review_complete = ReviewCompleteView.as_view()