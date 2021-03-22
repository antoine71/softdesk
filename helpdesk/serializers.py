from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Contributor, Project, Issue, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_password(self, password):
        return make_password(password)


class ContributorSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')
    # project = serializers.ReadOnlyField()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'permission', 'role']
        validators = [
            UniqueTogetherValidator(
                queryset=Contributor.objects.all(),
                fields=['user', 'project'],
            ),
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']


class IssueSerializer(serializers.ModelSerializer):

    issue_id = serializers.ReadOnlyField(source='id')
    author = serializers.ReadOnlyField(source='author.username')
    assignee = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username', default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'desc', 'tag', 'priority',
                  'status', 'author', 'assignee', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'created_time']
