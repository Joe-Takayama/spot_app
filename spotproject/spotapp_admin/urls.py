from django.urls import path
from .views import IndexView, LoginView, LogoutView, RegistselectView, updelView
 
app_name = 'spotapp_admin'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('Registselect/',RegistselectView.as_view(),name='Registselect'),
    path('updel/',updelView.as_view(), name='updel'),
]
