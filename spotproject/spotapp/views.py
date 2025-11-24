from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, 'spotapp/index.html')
    
class TekitoView(View):
    def get(self, request):
        return render(request, 'spotapp/tekito.html')
    
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
    
    
    
index = IndexView.as_view()
tekito = TekitoView.as_view()
signup = SignupView.signup
signup_complete = SignupCompleteView.as_view()