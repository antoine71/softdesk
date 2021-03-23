from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views


router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)

project_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project')
project_router.register(r'issues', views.IssueViewSet, basename='issues')
project_router.register(r'users', views.ContributorViewSet, basename='users')

issue_router = routers.NestedSimpleRouter(
    project_router, r'issues', lookup='issue')
issue_router.register(r'comments', views.CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
]
