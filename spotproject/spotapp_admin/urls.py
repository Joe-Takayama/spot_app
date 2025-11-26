from django.urls import path
from .views import IndexView, LoginView, LogoutView, RegistselectView, updelView, EventRegistrationView
 
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
    # イベント登録画面
    path('event_registration/', EventRegistrationView.as_view(), name='event_registration'),
    path('updel/',updelView.as_view(), name='updel'),
]
