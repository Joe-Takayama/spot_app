from django.urls import path
from . import views

app_name = "spotapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('signup/complete/', views.signup_complete, name="signup_complete"),
    path('spot/searchresult/',views.spot_searchresult,name="spot_searchresult"),
]
