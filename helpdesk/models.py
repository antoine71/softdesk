from django.db import models
from django.conf import settings


TYPE_CHOICES = (
    ('projet', 'Projet'),
    ('produit', 'Produit'),
    ('application', 'Application'),
)

PERMISSION_CHOICES = (
    ('manager', 'Manager'),
    ('contributeur', 'Contributeur'),
)

PRIORITY_CHOICES = (
    ('elevee', 'Élevée'),
    ('moyenne', 'Moyenne'),
    ('faible', 'Faible'),
)

STATUS_CHOICES = (
    ('a faire', 'À faire'),
    ('en cours', 'En Cours'),
    ('termine', 'Terminé')
)

TAG_CHOICES = (
    ('bug', 'Bug'),
    ('tache', 'Tâche'),
    ('amelioration', 'Amélioration'),
)


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    type = models.CharField(choices=TYPE_CHOICES, max_length=128)


class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(
        to=Project,
        related_name='contributors',
        on_delete=models.CASCADE)
    permission = models.CharField(choices=PERMISSION_CHOICES, max_length=128)
    role = models.CharField(max_length=128)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'], name='unique_user'),
        ]


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=2048)
    tag = models.CharField(choices=TAG_CHOICES, max_length=128)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=128)
    project = models.ForeignKey(
        to=Project,
        related_name='issues',
        on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=128)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='issue_author')
    assignee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='assignee', null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']


class Comment(models.Model):
    description = models.TextField(max_length=2048)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(
        to=Issue,
        related_name='comments',
        on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']
