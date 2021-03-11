from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from .models import Contributor, Project, Issue, Comment


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'permission', 'role']


class ProjectSerializer(serializers.ModelSerializer):

    issues = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Issue.objects.all())
    contributors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Contributor.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'issues',
                  'contributors']


class IssueSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    assignee = serializers.ReadOnlyField(source='assignee.username')
    comments = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Comment.objects.all())

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project',
                  'status', 'author', 'assignee', 'created_time', 'comments']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    issue = serializers.PrimaryKeyRelatedField(
        queryset=Issue.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue',
                  'created_time']

