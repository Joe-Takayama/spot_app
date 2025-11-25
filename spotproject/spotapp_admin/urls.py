from django.urls import path
from . import views

app_name = 'spotapp_admin'
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('Registselect/',views.Registselect,name='Registselect'),
    path('updel/',views.updel,name='updel'),
]
