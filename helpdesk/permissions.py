from rest_framework import permissions

from .models import Contributor, Project, Issue, Comment


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow author of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user


class IsProjectContributor(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS\
                                or request.method == 'POST':
            if isinstance(obj, Project):
                return Contributor.objects.filter(
                    user=request.user, project=obj).exists()
            elif isinstance(obj, Issue):
                return Contributor.objects.filter(
                    user=request.user, project=obj.project).exists()
            elif isinstance(obj, Comment):
                return Contributor.objects.filter(
                    user=request.user, project=obj.issue.project).exists()
        # Write permissions are only allowed to the author.
        else:
            return obj.author == request.user


class IsProjectManager(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method == 'POST':
            return True

        elif Contributor.objects.filter(
                user=request.user, project=obj).exists():

            if request.method in permissions.SAFE_METHODS:
                return True

            # Write permissions are only allowed to the project manager.
            else:
                return Contributor.objects.get(
                        user=request.user, project=obj).permission == 'manager'

        else:
            return False
