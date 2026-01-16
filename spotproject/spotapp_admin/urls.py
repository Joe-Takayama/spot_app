from django.urls import path
from .views import IndexView, LoginView, LogoutView, RegistselectView, UpdelView, EventRegistrationView, EventListView, EventUpdateView, EventDeleteView,SpotRegistrationView,SpotUpdateView,SpotDeleteView,SpotListView,OsiraseView, SpotSearchView, OsiraseDetailView
 
app_name = 'spotapp_admin'
urlpatterns = [
    # トップ画面
    path('', IndexView.as_view(), name="index"),
    # ログイン画面
    path('login/', LoginView.as_view(), name="login"),
    # ログアウト画面
    path('logout/', LogoutView.as_view(), name="logout"),
    # 登録選択画面
    path('Registselect/',RegistselectView.as_view(),name='Registselect'),
    #更新削除選択画面
    path('Updel/', UpdelView.as_view(),name='Updel'),
    # イベント一覧
    path('event_list/', EventListView.as_view(), name='event_list'),
    # イベント登録画面
    path('event_registration/', EventRegistrationView.as_view(), name='event_registration'),
    # イベント更新画面
    path('event_update/<uuid:event_id>/', EventUpdateView.as_view(), name='event_update'),
    # イベント削除画面
    path('event_delete/<uuid:event_id>/', EventDeleteView.as_view(), name='event_delete'),
    # 観光地一覧画面
    path('spot_list/', SpotListView.as_view(), name="spot_list"),
    #観光地登録画面
    path('spot_registration/',SpotRegistrationView.as_view(),name='spot_registration'),
    #観光地更新画面
    path('spot_update/<uuid:spot_id>/',SpotUpdateView.as_view(),name='spot_update'),
    #観光地削除画面
    path('spot_delete/<uuid:spot_id>/',SpotDeleteView.as_view(),name='spot_delete'),
    #お知らせ送信画面
    path('osirase/send/',OsiraseView.as_view(),name='osirase_send'),
    #お知らせ詳細
    path('osirase/<int:pk>/', OsiraseDetailView.as_view(), name='osirase_detail'),
    #観光地検索結果画面
    path('spot/result/', SpotSearchView.as_view(), name="search-result"),
]
