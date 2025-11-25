from django.shortcuts import render
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp_admin/index.html')
#登録選択画面
class RegistselectView(View):
    def get(self,request):
        return render(request,'spotapp_admin/Registrationselection.html')

    
index = IndexView.as_view() 
Registselect = RegistselectView.as_view()

