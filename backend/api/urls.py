
from django.urls import path, include
from .views import *



urlpatterns = [
    path('index/', index),
    path('posts/', posts_list),
#     path('posts/<int:post_id>/', post_detail),
#     path('posts/<int:post_id>/comments/', CommentsListAPIView.as_view()),
#     path('categories/<int:category_id>/posts/', posts_lists),

]

