from django.shortcuts import render, redirect
from django.views import View
from .forms import StaffForm
from .models import Staff
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout

#ホーム画面
class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp_admin/index.html')
#登録選択画面
class RegistselectView(View):
    def get(self,request):
        return render(request,'spotapp_admin/Registrationselection.html')
    

# ログイン画面
class LoginView(View):
    def get(self, request):
        form = StaffForm()
        return render(request, 'accounts/login_form.html', {'form': form})
    
    def post(self, request):
        form = StaffForm(request.POST)

        if not form.is_valid():
            return render(request, 'accounts/login_form.html', {'form': form})
        
        name = form.cleaned_data['name']
        password = form.cleaned_data['password']

        # 名前で検索
        try:
            staff = Staff.objects.get(name=name)
        except Staff.DoesNotExist:
            messages.error(request, '職員名が正しくありません')
            return render(request, 'accounts/login_form.html', {'form': form})
        
        # パスワード照合
        if check_password(password, staff.password):
            # ログイン成功
            request.session['staff_id'] = str(staff.staff_id)
            return redirect('spotapp_admin:index')
        
        # パスワード不一致
        messages.error(request, 'パスワードが違います')
        return render(request, 'accounts/login_form.html', {'form': form})

# ログアウト画面 
class LogoutView(View):
    def get(self, request):
        return render(request, 'accounts/logout.html')
    
    def post(self, request):
        logout(request)
        return redirect('spotapp_admin:index')

#更新削除選択画面
class updelView(View):
    def get(self,request):
        return render(request,'spotapp_admin/updatedelete.html')



    

