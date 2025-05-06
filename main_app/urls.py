from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('about/', views.about, name='about'),
    path('accounts/signup', views.signup, name='signup'),
    path('post-login-redirect/', views.post_login_redirect, name='post-login-redirect'),
    path('events/', views.events_index, name='events-index'),
    path('user-events/', views.user_events, name='user-events'),
    path('events/<int:event_id>/save/', views.save_event, name='save-event'),
    path('event/create/', views.add_event, name='event-create'),
    path('vendor-events/', views.vendor_events, name='vendor-events'),
    path('events/<int:event_id>/', views.event_detail, name='event-detail'),
    path('events/<int:event_id>/add-image', views.event_detail, name='add-image'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='event-update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='event-delete'),
    
]
