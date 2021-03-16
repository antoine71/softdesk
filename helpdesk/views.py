from rest_framework import permissions, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contributor, Project, Issue, Comment
from .serializers import (ContributorSerializer, ProjectSerializer,
                          IssueSerializer, CommentSerializer, UserSerializer)
from .permissions import IsProjectContributor, IsProjectManager


class CreateUserView(APIView):
    # Allow any user (authenticated or not) to access this url

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectManager]

    def create(self, request):
        serializer = ProjectSerializer(context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            contributor = Contributor(
                user=self.request.user,
                project=Project.objects.last(),
                permission='manager',
                role='Project Manager',
            )
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueViewSet(viewsets.ViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

    def list(self, request, project_pk=None):
        if not Project.objects.filter(pk=project_pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Issue.objects.filter(project=project_pk)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(pk=pk, project=project_pk)
        issue = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        serializer = IssueSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                project=Project.objects.get(pk=project_pk)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, project_pk=None):
        issue = Issue.objects.get(pk=pk)
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                project=Project.objects.get(pk=project_pk)
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(pk=pk, project=project_pk)
        issue = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, issue)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

    def list(self, request, project_pk=None, issue_pk=None):
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Comment.objects.filter(
            issue__project=project_pk,
            issue=issue_pk
        )
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(
            pk=pk,
            issue__project=project_pk,
            issue=issue_pk
        )
        comment = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request, project_pk=None, issue_pk=None):
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                issue=Issue.objects.get(pk=issue_pk)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, project_pk=None, issue_pk=None):
        comment = Comment.objects.get(pk=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                issue=Issue.objects.get(pk=issue_pk)
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(pk=pk, issue=issue_pk)
        comment = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewSet(viewsets.ViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, project_pk=None):
        if not Project.objects.filter(pk=project_pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset = Contributor.objects.filter(project=project_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None):
        queryset = Contributor.objects.filter(pk=pk, project=project_pk)
        contributor = get_object_or_404(queryset, pk=pk)
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        data = request.data.copy()
        data.update({'project': str(project_pk)})
        serializer = ContributorSerializer(data=data)
        if serializer.is_valid():
            print('test')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):
        queryset = Contributor.objects.filter(pk=pk, project=project_pk)
        contributor = get_object_or_404(queryset, pk=pk)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
