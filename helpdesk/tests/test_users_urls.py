import json

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from ..models import Project, Contributor


class UserUrlsTest(TestCase):

    def setUp(self):
        User.objects.create(username='user1', password=make_password('user1'))
        User.objects.create(username='user2', password=make_password('user2'))
        User.objects.create(username='user3', password=make_password('user3'))
        User.objects.create(username='user4', password=make_password('user4'))

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

        self.create_read_good_url = '/api/projects/1/users/'
        self.create_read_wrong_url = '/api/projects/3/users/'
        self.read_update_delete_good_url = '/api/projects/1/users/1/'
        self.read_update_delete_url_wrong_urls = [
            '/api/projects/2/users/2/',
            '/api/projects/3/users/2/',
            '/api/projects/1/users/4/',
            '/api/projects/2/users/1/',
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
        self.client_user4 = Client(
            HTTP_AUTHORIZATION='Bearer '+self.get_token('user4', 'user4')
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
        post = {'user': 'user4', 'permission': 'contributeur',
                'role': 'contributeur'}
        response = self.client_user1.post(self.create_read_good_url, post)
        self.assertEquals(response.status_code, 201)

    def test_create_wrong_url(self):
        post = {'user': 'user4', 'permission': 'contributeur',
                'role': 'contributeur'}
        response = self.client_user1.post(self.create_read_wrong_url, post)
        self.assertEquals(response.status_code, 404)

    def test_read_good_url(self):
        response = self.client_user1.get(self.read_update_delete_good_url)
        self.assertEquals(response.status_code, 405)

    def test_read_wrong_urls(self):
        for url in self.read_update_delete_url_wrong_urls:
            response = self.client_user1.get(url)
            self.assertEquals(response.status_code, 405)

    def test_update_good_url(self):
        post = {'user': 'user2', 'permission': 'contributeur',
                'role': 'contributeur'}
        response = self.client_user1.put(
            self.read_update_delete_good_url, post,
            content_type='application/json')
        self.assertEquals(response.status_code, 405)

    def test_update_wrong_urls(self):
        post = {'user': 'user2', 'permission': 'contributeur',
                'role': 'contributeur'}
        for url in self.read_update_delete_url_wrong_urls:
            response = self.client_user1.put(
                url, post, content_type='application/json')
            self.assertEquals(response.status_code, 405)

    def test_delete_wrong_urls(self):
        for url in self.read_update_delete_url_wrong_urls:
            response = self.client_user1.delete(url)
            self.assertEquals(response.status_code, 404)
