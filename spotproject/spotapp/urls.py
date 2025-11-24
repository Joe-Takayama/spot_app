from django.urls import path
from . import views

app_name = "spotapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('tekito/', views.tekito, name="tekito"),
    path('signup/', views.signup, name="signup"),
]
