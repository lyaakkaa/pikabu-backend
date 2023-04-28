from django.urls import path, include
from .views import *

urlpatterns = [
    path('posts/', posts_list),
    path('posts/<int:post_id>/', post_detail),
    path('categories/', categories_list),
    path('categories/<int:category_id>/posts/', posts_list_category),
    path('posts/<int:post_id>/comments/', CommentsListAPIView.as_view()),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentDetailAPIView.as_view()),
    path('users/', users_list),
    path('users/<int:user_id>/posts/', user_posts),
    path('users/<int:user_id>', user_detail),
    path('signin', SignInView.as_view()),
    path('signup', SignUpView.as_view()),
    path('likes', LikeView.as_view()),
]
