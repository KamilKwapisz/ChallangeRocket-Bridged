from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('flats/', views.flats_list, name='flats-list'),
    path('flat/<int:pk>', views.FlatDetailView.as_view(), name='flat-detail'),
    path('flat/<int:flat_id>/keypad', views.access_code, name='keypad'),
    path('room/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),
    path('room/<int:room_pk>/devices', views.host_device_permission, name='room-devices'),

    path('ajax/change_permission', views.ajax_change_device_permission, name='change-permission'),
    path('ajax/checkout-task', views.ajax_add_checkout_task, name='checkout-task'),
    path('ajax/validate-code', views.ajax_validate_access_code, name='validate-code'),
]