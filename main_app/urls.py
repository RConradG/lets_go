from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup', views.signup, name='signup'),
    path('collections/', views.collections_index, name='collections-index'),
    path('events/', views.events_index, name='events-index'),
    path('collections/<int:collection_id>', views.collection_detail, name='collection-detail'),
    path('collections/<int:event_id>', views.event_detail, name='event-detail'),
    path('collections/create/', views.CollectionCreate.as_view(), name='collection-create'),
    path('event/create/', views.add_event, name='event-create'),
    path('events/<int:event_id>>', views.event_detail, name='event-detail'),
    path('collections/<int:pk>/update/', views.CollectionUpdate.as_view(), name='collection-update'),
    path('collections/<int:pk>/delete/', views.CollectionDelete.as_view(), name='collection-delete'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='event-update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='event-delete'),
    path('collections/<int:collection_id>/add-item/', views.add_item, name='add-item'),
    path('item/<int:pk>/update/', views.ItemUpdate.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', views.ItemDelete.as_view(), name='item-delete'),
    
]
