from django.urls import path
from . import views
from .views import ContactView
 
 
app_name = "spotapp"
 
urlpatterns = [
    path('', views.index, name="index"),
 
    path('signup/', views.signup, name="signup"),
    path('signup/complete/', views.signup_complete, name="signup_complete"),
 
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('profile_edit/complete/', views.profile_edit_complete, name='profile_edit_complete'),
 
    path('password/change/', views.PasswordChangeView.as_view(), name="password_change"),
    path('password/change/complete/', views.PasswordChangeCompleteView.as_view(), name="password_change_complete"),
 
    #観光地検索結果画面
    path('spot/searchresult/',views.spot_searchresult,name="spot_searchresult"),
    #観光地詳細画面
    path('spot/detail/',views.spot_detail,name="spot_detail"),
 
    #レビュー投稿画面
    path('review/create/',views.review_create,name="review_create"),
    #レビュー投稿完了画面
    path('review/complete/',views.review_complete,name="review_complete"),
 
    path('favorite/list/', views.FavoriteListView.as_view(), name="favorite_list"),
   
    path('event/chart/', views.event_chart, name='event_chart'),
    path('event/detail/', views.event_detail, name='event_detail'),
 
    #お問い合わせ画面
    path('contact/', ContactView.as_view(),name="contact"),
    path('contact/complete', views.contact_complete, name='contact_complete'),
 
]