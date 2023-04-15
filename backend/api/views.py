from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse('check')


@api_view(['GET'])
def posts_list(request):
    posts = Post.objects.all()
    serializers = PostSerializer(posts, many=True)
    return Response(serializers.data)
