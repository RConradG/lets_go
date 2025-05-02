from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup', views.signup, name='signup'),
    path('collections/', views.collections_index, name='collections-index'),
    path('collections/<int:collection_id>', views.collection_detail, name='collection-detail'),
    path('collections/create/', views.CollectionCreate.as_view(), name='collection-create'),
    path('collections/<int:pk>/update/', views.CollectionUpdate.as_view(), name='collection-update'),
    path('collections/<int:pk>/delete/', views.CollectionDelete.as_view(), name='collection-delete'),
    path('collections/<int:collection_id>/add-item/', views.add_item, name='add-item'),
    path('item/<int:pk>/update/', views.ItemUpdate.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', views.ItemDelete.as_view(), name='item-delete'),
    
]
