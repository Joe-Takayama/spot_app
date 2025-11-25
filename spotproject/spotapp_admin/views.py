from django.shortcuts import render
from django.views import View
from .forms import StaffForm
from .models import Staff
from django.contrib import messages
from django.contrib.auth.hashers import check_password


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

            return render(request, 'accounts/login_success.html', {'statt': staff})
        
        # パスワード不一致
        messages.error(request, 'パスワードが違います')
        return render(request, 'accounts/login_form.html', {'form': form})

#更新削除選択画面
class updelView(View):
    def get(self,request):
        return render(request,'spotapp_admin/updatedelete.html')



    
index = IndexView.as_view() 
login = LoginView.as_view()
Registselect = RegistselectView.as_view()
updel = updelView.as_view()

