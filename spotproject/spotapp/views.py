from django.shortcuts import render
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp/index.html')
    
class TekitoView(View):
    def get(self, request):
        return render(request, 'spotapp/tekito.html')
    
    
index = IndexView.as_view()
tekito = TekitoView.as_view()