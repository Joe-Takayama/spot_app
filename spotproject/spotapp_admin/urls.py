from django.urls import path
from . import views

app_name = 'spotapp_admin'
urlpatterns = [
    path('', views.index, name="index"),
    path('Registselect',views.Registselect,name='Registselect')
]
