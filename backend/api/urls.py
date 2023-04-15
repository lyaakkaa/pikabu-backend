
from django.urls import path, include
from .views import *



urlpatterns = [
    path('index/', index),
    path('posts/', posts_list),
    path('posts/<int:post_id>/', post_detail),
    path('categories/', categories_list),
    path('categories/<int:category_id>/posts/', posts_list_category),
    path('posts/<int:post_id>/comments/', CommentsListAPIView.as_view()),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentDetailAPIView.as_view()),
    path('users/', UsersListAPIView.as_view()),
    path('users/<int:pk>/', UserDetailAPIView.as_view()),

]

