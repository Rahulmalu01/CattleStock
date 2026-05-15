from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='articles'),
    path('create/', views.create_article, name='create_article'),
    path('moderation/', views.moderation_dashboard, name='moderation_dashboard'),
    path('approve/<str:article_id>/', views.approve_article, name='approve_article'),
    path('reject/<str:article_id>/', views.reject_article, name='reject_article'),
    path('edit/<str:article_id>/', views.edit_article, name='edit_article'),
    path('remove/<str:article_id>/', views.user_delete_article, name='user_delete_article'),
    path('<str:article_id>/', views.article_detail, name='article_detail'),
    path('bookmark/<str:article_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('like/<str:article_id>/', views.toggle_like, name='toggle_like'),
    path('comment/<str:article_id>/', views.add_comment, name='add_comment'),
]