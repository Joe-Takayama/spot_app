from django.urls import path
from . import views

app_name = "spotapp"

urlpatterns = [
    path('', views.index, name="index"),

    path('signup/', views.signup, name="signup"),
    path('signup/complete/', views.signup_complete, name="signup_complete"),

    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('profile_edit/complete/', views.profile_edit_complete, name='profile_edit_complete'),

    path('password_change/', views.password_change, name="password_change"),
    path('password_change/complete/', views.password_change_complete, name="password_change_complete"),

    path('spot/searchresult/',views.spot_searchresult,name="spot_searchresult"),
    path('spot/detail/',views.spot_detail,name="spot_detail"), 

    path('review/create/',views.review_create,name="review_create"),
    path('review/complete/',views.review_complete,name="review_complete"),

    path('favorite/list/', views.FavoriteListView.as_view(), name="favorite_list"),
]

