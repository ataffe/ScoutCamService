import json

from django.test import TestCase
from rest_framework.test import APIClient

from rules.models import Camera, Rule, User


class UserDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Alice', email='alice@example.com', password='secret123'
        )

    def test_get_user_returns_correct_data(self):
        response = self.client.get(f'/v1/user/{self.user.pk}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'Alice')
        self.assertEqual(data['email'], 'alice@example.com')

    def test_get_user_not_found_returns_404(self):
        response = self.client.get('/v1/user/9999')
        self.assertEqual(response.status_code, 404)

    def test_create_user_returns_201_and_persists(self):
        payload = {'name': 'Bob', 'email': 'bob@example.com', 'password': 'pass456'}
        response = self.client.post(
            '/v1/user/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Bob')
        self.assertTrue(User.objects.filter(email='bob@example.com').exists())

    def test_create_user_missing_required_fields_returns_400(self):
        response = self.client.post(
            '/v1/user/',
            data=json.dumps({'name': 'Bob'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_user_returns_204_and_removes_record(self):
        response = self.client.delete(f'/v1/user/{self.user.pk}')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_delete_user_not_found_returns_404(self):
        response = self.client.delete('/v1/user/9999')
        self.assertEqual(response.status_code, 404)


class UserListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create(name='Alice', email='alice@example.com', password='pass')
        User.objects.create(name='Bob', email='bob@example.com', password='pass')

    def test_list_users_returns_all(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_list_users_empty(self):
        User.objects.all().delete()
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class RuleDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Alice', email='alice@example.com', password='pass'
        )
        self.camera = Camera.objects.create(
            user_id=self.user, cam_number=1, location='Front door'
        )
        self.rule = Rule.objects.create(
            user_id=self.user, rule='Notify on motion', camera_id=self.camera
        )

    def test_get_rule_returns_correct_data(self):
        response = self.client.get(f'/v1/rule/{self.rule.pk}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['rule'], 'Notify on motion')

    def test_get_rule_not_found_returns_404(self):
        response = self.client.get('/v1/rule/9999')
        self.assertEqual(response.status_code, 404)

    def test_create_rule_returns_201_and_persists(self):
        payload = {
            'user_id': self.user.pk,
            'rule': 'Notify on sound',
            'camera_id': self.camera.pk,
        }
        response = self.client.post(
            '/v1/rule/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Rule.objects.filter(rule='Notify on sound').exists())

    def test_create_rule_missing_required_fields_returns_400(self):
        response = self.client.post(
            '/v1/rule/',
            data=json.dumps({'rule': 'Notify on sound'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_rule_returns_204_and_removes_record(self):
        response = self.client.delete(f'/v1/rule/{self.rule.pk}')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Rule.objects.filter(pk=self.rule.pk).exists())

    def test_delete_rule_not_found_returns_404(self):
        response = self.client.delete('/v1/rule/9999')
        self.assertEqual(response.status_code, 404)


class RuleListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Alice', email='alice@example.com', password='pass'
        )
        other_user = User.objects.create(
            name='Bob', email='bob@example.com', password='pass'
        )
        self.camera = Camera.objects.create(
            user_id=self.user, cam_number=1, location='Front door'
        )
        Rule.objects.create(user_id=self.user, rule='Rule 1', camera_id=self.camera)
        Rule.objects.create(user_id=self.user, rule='Rule 2', camera_id=self.camera)
        Rule.objects.create(user_id=other_user, rule='Other rule', camera_id=self.camera)

    def test_list_rules_for_user_returns_only_their_rules(self):
        response = self.client.get(f'/v1/rules/user/{self.user.pk}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertTrue(all(r['user_id'] == self.user.pk for r in data))

    def test_list_rules_for_nonexistent_user_returns_empty(self):
        response = self.client.get('/v1/rules/user/9999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class CameraDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Alice', email='alice@example.com', password='pass'
        )
        self.camera = Camera.objects.create(
            user_id=self.user, cam_number=1, location='Front door'
        )

    def test_get_camera_returns_correct_data(self):
        response = self.client.get(f'/v1/camera/{self.camera.pk}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['location'], 'Front door')
        self.assertEqual(data['cam_number'], 1)

    def test_get_camera_not_found_returns_404(self):
        response = self.client.get('/v1/camera/9999')
        self.assertEqual(response.status_code, 404)

    def test_create_camera_returns_201_and_persists(self):
        payload = {'user_id': self.user.pk, 'cam_number': 2, 'location': 'Back yard'}
        response = self.client.post(
            '/v1/camera/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Camera.objects.filter(location='Back yard').exists())

    def test_create_camera_missing_required_fields_returns_400(self):
        response = self.client.post(
            '/v1/camera/',
            data=json.dumps({'location': 'Back yard'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_camera_returns_204_and_removes_record(self):
        response = self.client.delete(f'/v1/camera/{self.camera.pk}')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Camera.objects.filter(pk=self.camera.pk).exists())

    def test_delete_camera_not_found_returns_404(self):
        response = self.client.delete('/v1/camera/9999')
        self.assertEqual(response.status_code, 404)


class CameraListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Alice', email='alice@example.com', password='pass'
        )
        other_user = User.objects.create(
            name='Bob', email='bob@example.com', password='pass'
        )
        Camera.objects.create(user_id=self.user, cam_number=1, location='Front door')
        Camera.objects.create(user_id=self.user, cam_number=2, location='Back yard')
        Camera.objects.create(user_id=other_user, cam_number=3, location='Garage')

    def test_list_cameras_for_user_returns_only_their_cameras(self):
        response = self.client.get(f'/v1/cameras/user/{self.user.pk}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertTrue(all(c['user_id'] == self.user.pk for c in data))