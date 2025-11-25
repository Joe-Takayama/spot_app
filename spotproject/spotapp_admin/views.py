from django.shortcuts import render
from django.views import View
from .forms import StaffForm


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
        return render(request, 'spotapp_admin/login_form.html', {'form': form})
    



    
index = IndexView.as_view() 
login = LoginView.as_view()
Registselect = RegistselectView.as_view()

