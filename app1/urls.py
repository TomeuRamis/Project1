
#urls go here
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "app1"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name="login"),
    path('home/', views.logged, name="logged"),
    path('requestProcess/', views.request_process, name='requestProcess'),
    path('requestSuccessful/', views.request_successful, name='request_successful'),
    path('requestSuccessful', views.post, name='post')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
