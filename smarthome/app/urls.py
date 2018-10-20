from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    # path('lokal/<int:pk>', views.lokal_detail_view, name='lokal-detail'),
]