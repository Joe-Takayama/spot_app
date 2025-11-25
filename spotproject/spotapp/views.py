from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileEditForm

class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp/index.html')
    
#  新規登録ビュー   
class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "spotapp/signup.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
        user = request.user
        form = ProfileEditForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("spotapp:profile_edit_complete")

        return render(request, "spotapp/profile_edit.html", {"form": form})


# プロフィール編集完了ビュー
class ProfileEditCompleteView(LoginRequiredMixin, View):
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

signup = SignupView.as_view()
signup_complete = SignupCompleteView.as_view()

profile_edit = ProfileEditView.as_view()
profile_edit_complete = ProfileEditCompleteView.as_view()

spot_searchresult = SpotSearchResultView.as_view()
spot_detail = SpotDetailView.as_view()

review_create = ReviewCreateView.as_view()
review_complete = ReviewCompleteView.as_view()