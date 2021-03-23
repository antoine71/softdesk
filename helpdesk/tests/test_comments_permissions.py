import json

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from ..models import Project, Contributor, Issue, Comment


class CommentPermissionsTest(TestCase):

    def setUp(self):
        User.objects.create(username='user1', password=make_password('user1'))
        User.objects.create(username='user2', password=make_password('user2'))
        User.objects.create(username='user3', password=make_password('user3'))

        Project.objects.create(title='title1', description='description1',
                               type='projet')
        Project.objects.create(title='title2', description='a description 2',
                               type='projet')

        Contributor.objects.create(
            user=User.objects.get(pk=1),
            project=Project.objects.get(pk=1),
            permission='manager',
            role='manager',
        )

        Contributor.objects.create(
            user=User.objects.get(pk=2),
            project=Project.objects.get(pk=1),
            permission='contributeur',
            role='contributeur',
        )

        Issue.objects.create(
            title='title1',
            desc='description1',
            tag='bug',
            priority='moyenne',
            project=Project.objects.get(pk=1),
            status='a faire',
            author=User.objects.get(pk=1),
            assignee=User.objects.get(pk=2),
            created_time=0,
        )

        Issue.objects.create(
            title='title2',
            desc='description2',
            tag='bug',
            priority='moyenne',
            project=Project.objects.get(pk=1),
            status='a faire',
            author=User.objects.get(pk=1),
            assignee=User.objects.get(pk=2),
            created_time=0,
        )
        Issue.objects.create(
            title='title4',
            desc='description4',
            tag='bug',
            priority='moyenne',
            project=Project.objects.get(pk=2),
            status='a faire',
            author=User.objects.get(pk=1),
            assignee=User.objects.get(pk=2),
            created_time=0,
        )

        Comment.objects.create(
            description='description1',
            author=User.objects.get(pk=1),
            issue=Issue.objects.get(pk=1),
            created_time=0,
        )

        Comment.objects.create(
            description='description2',
            author=User.objects.get(pk=2),
            issue=Issue.objects.get(pk=1),
            created_time=0,
        )

        Comment.objects.create(
            description='description3',
            author=User.objects.get(pk=1),
            issue=Issue.objects.get(pk=3),
            created_time=0,
        )

        self.create_read_url = '/api/projects/1/issues/1/comments/'
        self.read_update_delete_url = '/api/projects/1/issues/1/comments/1/'
        self.auth_url = reverse('token_obtain')

        self.client_user1 = Client(
            HTTP_AUTHORIZATION='Bearer '+self.get_token('user1', 'user1')
            )
        self.client_user2 = Client(
            HTTP_AUTHORIZATION='Bearer '+self.get_token('user2', 'user2')
            )
        self.client_user3 = Client(
            HTTP_AUTHORIZATION='Bearer '+self.get_token('user3', 'user3')
            )

    def get_token(self, username, password):
        post = {'username': username, 'password': password}
        response = self.client.post(self.auth_url, post)
        data = json.loads(response.content)
        return data['access']

    def test_list_contributor(self):
        response = self.client_user1.get(self.create_read_url)
        self.assertContains(response, 'description1')
        self.assertContains(response, 'description2')

    def test_list_non_contributor(self):
        response = self.client_user3.get(self.create_read_url)
        self.assertEquals(response.status_code, 403)

    def test_create_contributor(self):
        post = {'description': 'description4'}
        response = self.client_user1.post(self.create_read_url, post)
        self.assertEquals(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEquals(data['description'], 'description4')
        self.assertEquals(Comment.objects.filter(issue=1).count(), 3)

    def test_create_non_contributor(self):
        post = {'description': 'description4'}
        response = self.client_user3.post(self.create_read_url, post)
        self.assertEquals(response.status_code, 403)

    def test_read_contributor(self):
        response = self.client_user1.get(self.read_update_delete_url)
        self.assertContains(response, 'description1')

    def test_update_author(self):
        post = {'description': 'description_update'}
        response = self.client_user1.put(
            self.read_update_delete_url, post, content_type='application/json')
        self.assertContains(response, 'description_update')

    def test_update_non_author(self):
        post = {'description': 'description_update'}
        response = self.client_user2.put(
            self.read_update_delete_url, post, content_type='application/json')
        self.assertEquals(response.status_code, 403)

    def test_delete_author(self):
        response = self.client_user1.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Comment.objects.filter(issue=1).count(), 1)

    def test_delete_non_author(self):
        response = self.client_user2.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, 403)
