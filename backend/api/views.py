from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework_jwt.utils import jwt_encode_handler, jwt_decode_handler
from django.contrib.auth import authenticate
from .models import PeekabooUser
from .serializers import PeekabooUserSerializer
from datetime import datetime, timedelta


# Create your views here.

def index(request):
    return HttpResponse('check')

@api_view(['GET', 'POST'])
def posts_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializers = PostSerializer(posts, many=True)
        return Response(serializers.data, status=200)
    elif request.method == 'POST':
        if is_token_exp(request):
            return Response({'message': 'unauthorized'}, status=401)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'DELETE', 'PUT'])
def post_detail(request, post_id):
    if is_token_exp(request):
        return Response({'message': 'unauthorized'}, status=401) 
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist as err:
        return JsonResponse({'message': str(err)}, status=400)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=200)
    if request.method == 'DELETE':
        post.delete()
        return Response({'message': 'delete post ' + str(post.pk)})

    if request.method == 'PUT':
        serializer = PostSerializer(data=request.data, instance=post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


@api_view(['GET', 'POST'])
def categories_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializers = CategorySerializer(categories, many=True)
        return Response(serializers.data, status=200)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def posts_list_category(request, category_id):
    try:
        posts = Post.objects.filter(category=category_id)
    except Post.DoesNotExist as err:
        return JsonResponse({'message': str(err)}, status=400)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=200)


class CommentsListAPIView(APIView):
    def get_comments(self, post_id):
        try:
            comments = Comment.objects.filter(post=post_id)
            return comments
        except Comment.DoesNotExist as err:
            return Response({'error': 'Object does not exists'})

    def get(self, request, post_id=None):
        comments = self.get_comments(post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, post_id):
        if is_token_exp(request):
            return Response({'message': 'unauthorized'}, status=401)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CommentDetailAPIView(APIView):
    def get_comment(self, pk):
        try:
            comment = Comment.objects.get(id=pk)
            return comment
        except Comment.DoesNotExist as err:
            return Response({'error': 'Object does not exists'})

    def get(self, request, post_id=None, pk=None):
        comment = self.get_comment(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=200)

    def put(self, request, post_id=None, pk=None):
        comment = self.get_comment(pk)
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, post_id=None, pk=None):
        comment = self.get_comment(pk)
        comment.delete()
        return Response({'message': 'delete comment ' + str(comment)})


class SignInView(APIView):
    def post(self, request):
        usr = request.data.get('username')
        psd = request.data.get('password')

        user = PeekabooUser.objects.filter(username=usr, password=psd).first()
        if not user:
            return Response({'error': 'Invalid credentials'})

        token = jwt_encode_handler(
            {'user_id': user.pk, 'exp_time': int((datetime.now() + timedelta(days=1)).timestamp())})

        return Response({
            'token': str(token),
            'id': user.id,
        })


class SignUpView(APIView):
    def post(self, request):
        serializer = PeekabooUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = jwt_encode_handler(
                {'user_id': user.pk, 'exp_time': int((datetime.now() + timedelta(days=1)).timestamp())})

            return Response({
                'token': str(token),
                'id': user.id,
            })

        return Response(serializer.errors, status=400)


def is_token_exp(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if(auth_header != None):
        token = auth_header.split()[-1]
        decoded = jwt_decode_handler(token)
        exp_time = decoded['exp_time']
        if int(datetime.now().timestamp()) >= exp_time:
            return True
    return False



@api_view(['GET'])
def users_list(request):
    if request.method == 'GET':
        users = PeekabooUser.objects.all()
        serializers = PeekabooUserSerializer(users, many=True)
        return Response(serializers.data, status=200)


@api_view(['GET'])
def user_detail(request, user_id):
    try:
        user = PeekabooUser.objects.get(id=user_id)
    except PeekabooUser.DoesNotExist as err:
        return JsonResponse({'message': str(err)}, status=400)

    if request.method == 'GET':
        serializer = PeekabooUserSerializer(user)
        return Response(serializer.data, status=200)
