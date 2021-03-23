import json

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from ..models import Project, Contributor


class UserPermissionsTest(TestCase):

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

        self.create_read_url = '/api/projects/1/users/'
        self.read_update_delete_url = '/api/projects/1/users/1/'
        self.read_update_delete_url_contributor = '/api/projects/1/users/2/'
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

    def test_list_manager(self):
        response = self.client_user1.get(self.create_read_url)
        self.assertContains(response, 'manager')
        self.assertContains(response, 'contributeur')

    def test_list_contributor(self):
        response = self.client_user2.get(self.create_read_url)
        self.assertContains(response, 'manager')
        self.assertContains(response, 'contributeur')

    def test_list_non_contributor(self):
        response = self.client_user3.get(self.create_read_url)
        self.assertEquals(response.status_code, 403)

    def test_create_manager(self):
        post = {'user': 'user4', 'permission': 'contributeur',
                'role': 'contributeur'}
        response = self.client_user1.post(self.create_read_url, post)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Contributor.objects.filter(project=1).count(), 3)

    def test_create_contributor(self):
        post = {'user': 'user4', 'permission': 'contributeur',
                'role': 'contributeur'}
        response = self.client_user2.post(self.create_read_url, post)
        self.assertEquals(response.status_code, 403)

    def test_create_non_contributor(self):
        post = {'user': 'user4', 'permission': 'contributeur',
                'role': 'contributeur'}
        response = self.client_user3.post(self.create_read_url, post)
        self.assertEquals(response.status_code, 403)

    def test_read_manager(self):
        response = self.client_user1.get(self.read_update_delete_url)
        self.assertEquals(response.status_code, 405)

    def test_update_manager(self):
        post = {'user': 'user2', 'permission': 'contributeur',
                'role': 'contributeur'}
        response = self.client_user1.put(
            self.read_update_delete_url, post, content_type='application/json')
        self.assertEquals(response.status_code, 405)

    def test_delete_manager_one_manager_only(self):
        response = self.client_user1.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, 403)

    def test_delete_manager_contributor(self):
        response = self.client_user1.delete(self.read_update_delete_url_contributor)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Contributor.objects.filter(
            project=1, permission='contributor').count(), 0)
        self.assertEquals(Contributor.objects.filter(project=1).count(), 1)

    def test_delete_manager_more_than_one_manager_only(self):
        Contributor.objects.create(
            user=User.objects.get(pk=3),
            project=Project.objects.get(pk=1),
            permission='manager',
            role='manager',
        )
        response = self.client_user1.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Contributor.objects.filter(
            project=1, permission='manager').count(), 1)
        self.assertEquals(Contributor.objects.filter(project=1).count(), 2)

    def test_delete_contributor(self):
        response = self.client_user2.delete(
            self.read_update_delete_url_contributor)
        self.assertEquals(response.status_code, 403)

    def test_delete_non_contributor(self):
        response = self.client_user4.delete(
            self.read_update_delete_url_contributor)
        self.assertEquals(response.status_code, 403)
