from django.urls import path
from . import views
from .views import ContactView, LoginView, LogoutView,SpotDetailView

app_name = "spotapp"

urlpatterns = [
    path('', views.index, name="index"),

    path('signup/', views.signup, name="signup"),
    path('signup/complete/', views.signup_complete, name="signup_complete"),

    path("profile/", views.profile_view, name="profile"),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('profile_edit/complete/', views.profile_edit_complete, name='profile_edit_complete'),

    path('password/change/', views.PasswordChangeView.as_view(), name="password_change"),
    path('password/change/complete/', views.PasswordChangeCompleteView.as_view(), name="password_change_complete"),

    # 観光地検索結果画面
    path('spot/searchresult/', views.spot_searchresult, name="spot_searchresult"),

    # 観光地詳細画面
    path('spot/<uuid:spot_id>/',views. SpotDetailView.as_view(), name='spot_detail'),

    # レビュー投稿画面
    path('review/create/<uuid:spot_id>/',views.review_create,name="review_create"),

    # レビュー投稿完了画面
    path('review/complete/', views.review_complete, name="review_complete"),

    path('review/detail/', views.review_detail, name="review_detail"),

    path('favorite/list/', views.FavoriteListView.as_view(), name="favorite_list"),

    path('event/chart/', views.event_chart, name='event_chart'),  # イベント一覧（OK）

    # 🔧 修正箇所：<uuid:event_id> を追加して、イベントごとの詳細ページを表示できるように修正！
    path('event/detail/<uuid:event_id>/', views.event_detail, name='event_detail'),  # ← 修正済み！

    # お問い合わせ画面
    path('contact/', ContactView.as_view(), name="contact"),
    path('contact/complete', views.contact_complete, name='contact_complete'),

    # ログイン画面
    path('login/', LoginView.as_view(), name="login"),

    # ログアウト画面
    path('logout/', views.LogoutView.as_view(), name="logout"),
]
