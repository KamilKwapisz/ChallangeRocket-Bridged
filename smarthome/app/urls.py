from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('lokal/<int:pk>', views.lokal_detail_view, name='lokal-detail'),
]