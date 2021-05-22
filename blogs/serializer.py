from django.db import models
from django.db.models import fields
from rest_framework import serializers
from blogs.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
