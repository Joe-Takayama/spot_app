from django.urls import path
from . import views

app_name = "spotapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('signup/complete/', views.signup_complete, name="signup_complete"),
    path('spot/searchresult/',views.spot_searchresult,name="spot_searchresult"),
    path('spot/detail/',views.spot_detail,name="spot_detail"), 
    path('review/create/',views.review_create,name="review_create"),
    path('review/complete/',views.review_complete,name="review_complete"),
]
#今日の夕飯は麻婆豆腐です。