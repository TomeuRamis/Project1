
#urls go here

from django.urls import path
from . import views

app_name = "app1"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name="login"),
    path('logged/', views.logged, name="logged"),
    path('requestProcess/', views.requestprocess, name='requestProcess')
]