
from django.urls import path, include
from .views import *
from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )




urlpatterns = [
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', posts_list),
    path('posts/<int:post_id>/', post_detail),
    path('categories/', categories_list),
    path('categories/<int:category_id>/posts/', posts_list_category),
    path('posts/<int:post_id>/comments/', CommentsListAPIView.as_view()),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentDetailAPIView.as_view()),
    path('users/', UsersListAPIView.as_view()),
    path('users/<int:pk>/', UserDetailAPIView.as_view()),
    path('login/', obtain_jwt_token),
    path('register/', RegistrationAPIView.as_view()),  # post (token)
]

