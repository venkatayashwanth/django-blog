from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.create_post, name='create_post'),
    path('edit/<int:pk>', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
]