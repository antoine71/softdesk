import json

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from ..models import Project, Contributor, Issue, Comment


class IssueUrlsTest(TestCase):

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

        self.create_read_good_url = '/api/projects/1/issues/'
        self.create_read_wrong_url = '/api/projects/4/issues/'
        self.read_update_delete_good_url = '/api/projects/1/issues/1/'
        self.read_update_delete_wrong_urls = [
            '/api/projects/2/issues/1/',
            '/api/projects/1/issues/3/',
            '/api/projects/3/issues/1/',
            '/api/projects/1/issues/5/',
        ]
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

    def test_list_good_url(self):
        response = self.client_user1.get(self.create_read_good_url)
        self.assertEquals(response.status_code, 200)

    def test_list_wrong_url(self):
        response = self.client_user1.get(self.create_read_wrong_url)
        self.assertEquals(response.status_code, 404)

    def test_create_good_url(self):
        post = {'title': 'title3', 'desc': 'description3',
                'tag': 'bug', 'priority': 'moyenne', 'status': 'en cours',
                'assignee': 'user2'}
        response = self.client_user1.post(self.create_read_good_url, post)
        self.assertEquals(response.status_code, 201)

    def test_create_wrong_url(self):
        post = {'title': 'title3', 'desc': 'description3',
                'tag': 'bug', 'priority': 'moyenne', 'status': 'en cours',
                'assignee': 'user2'}
        response = self.client_user1.post(self.create_read_wrong_url, post)
        self.assertEquals(response.status_code, 404)

    def test_read_good_url(self):
        response = self.client_user1.get(self.read_update_delete_good_url)
        self.assertEquals(response.status_code, 200)

    def test_read_wrong_urls(self):
        for url in self.read_update_delete_wrong_urls:
            response = self.client_user1.get(url)
            self.assertEquals(response.status_code, 404)

    def test_update_good_url(self):
        post = {'title': 'title_update', 'desc': 'description',
                'tag': 'bug', 'priority': 'moyenne', 'status': 'en cours',
                'assignee': 'user2'}
        response = self.client_user1.put(self.read_update_delete_good_url, post, content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_update_wrong_urls(self):
        post = {'title': 'title_update', 'desc': 'description',
                'tag': 'bug', 'priority': 'moyenne', 'status': 'en cours',
                'assignee': 'user2'}
        for url in self.read_update_delete_wrong_urls:
            response = self.client_user1.put(url, post, content_type='application/json')
            self.assertEquals(response.status_code, 404)

    def test_delete_good_url(self):
        response = self.client_user1.delete(self.read_update_delete_good_url)
        self.assertEquals(response.status_code, 204)

    def test_delete_wrong_urls(self):
        for url in self.read_update_delete_wrong_urls:
            response = self.client_user1.delete(url)
            self.assertEquals(response.status_code, 404)
