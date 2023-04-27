
from rest_framework import serializers
from .models import *


class PeekabooUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeekabooUser
        fields = ['id', 'username', 'total_rating', 'role', 'password']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_username', 'created_date', 'body', 'category', 'like_count']

    def get_like_count(self, obj):
        return Like.objects.filter(post_id=obj.id, liked=True).count() - Like.objects.filter(post_id=obj.id, liked=False).count()

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


