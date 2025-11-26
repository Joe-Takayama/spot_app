from django.urls import path
from .views import IndexView, LoginView, LogoutView, RegistselectView, updelView, EventRegistrationView, EventListView, EventUpdateView, EventDeleteView
 
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
    path('updel/',updelView.as_view(),name='updel'),
    # イベント一覧
    path('event_list/', EventListView.as_view(), name='event_list'),
    # イベント登録画面
    path('event_registration/', EventRegistrationView.as_view(), name='event_registration'),
    # イベント更新画面
    path('event_update/<uuid:event_id>/', EventUpdateView.as_view(), name='event_update'),
    # イベント削除画面
    path('event_delete/<uuid:event_id>/', EventDeleteView.as_view(), name='event_delete'),
]
