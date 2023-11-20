from django.contrib import admin
from django.urls import path, include
from firstApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('index/', views.result, name='result'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('', views.index_deep, name='deep'),    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
