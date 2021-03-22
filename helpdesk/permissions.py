from rest_framework import permissions

from .models import Contributor, Project, Issue, Comment


class IsProjectContributor(permissions.BasePermission):
    """
    Custom permission to only allow project contributors to create or view
    issues or comments, and only author to edit or delete issues and comments.
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
    Custom permission to only allow project manager to edit or delete
    a project, and create or delete project users.
    """

    def has_object_permission(self, request, view, obj):
        # Creation of a new project is allowed to any registered user
        if request.method == 'POST':
            return True

        elif Contributor.objects.filter(
                user=request.user, project=obj).exists():
            # View a project is only allowed to the project contributors.
            if request.method in permissions.SAFE_METHODS:
                return True

            # Write permissions are only allowed to the project manager.
            else:
                return Contributor.objects.get(
                        user=request.user, project=obj).permission == 'manager'

        else:
            return False


class IsProjectManagerUser(permissions.BasePermission):
    """
    Custom permission to only allow only project manager to create or delete
    project users, and project contributors to view project users.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to project contributors
        if request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(
                    user=request.user, project=obj).exists()

        # Delete is only allowed to project manager if there is at least 2
        # project managers registered for the project
        elif request.method == 'DELETE':
            return Contributor.objects.filter(
                    user=request.user, project=obj.project,
                    permission='manager').exists() \
                    and (Contributor.objects.filter(
                        permission='manager', project=obj.project).count() > 1
                        or obj.permission == 'contributeur')

        # Create is only allowed to project manager
        elif request.method == 'POST':
            return Contributor.objects.filter(
                    user=request.user, project=obj, permission='manager'
                    ).exists()
        else:
            return False
