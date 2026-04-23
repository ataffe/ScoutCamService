from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

from rules.models import Camera, Rule, User


def make_user(username, email, password='StrongPass123!', first_name='Test', last_name='User'):
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User',
        )

    def get_jwt_token(self, user):
        """Helper to generate a JWT token for a given user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate(self, user):
        """Helper to set the JWT token on the client."""
        token = self.get_jwt_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_delete_user_success(self):
        self.authenticate(self.user)
        response = self.client.delete(
            reverse('v1:user_detail', kwargs={'public_user_id': self.user.public_user_id}),
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(public_user_id=self.user.public_user_id).exists())

    def test_delete_user_not_found(self):
        self.authenticate(self.user)
        response = self.client.delete(
            reverse('v1:user_detail', kwargs={'public_user_id': uuid.uuid4()}),
        )
        self.assertEqual(response.status_code, 404)

    def test_get_user_success(self):
        self.authenticate(self.user)
        response = self.client.get(
            reverse('v1:user_detail', kwargs={'public_user_id': self.user.public_user_id}),
        )
        self.assertEqual(response.status_code, 200)
        user_returned = response.json()
        self.assertEqual(user_returned['public_user_id'], str(self.user.public_user_id))

    def test_get_user_not_found(self):
        self.authenticate(self.user)
        response = self.client.get(
            reverse('v1:user_detail', kwargs={'public_user_id': uuid.uuid4()}),
        )
        self.assertEqual(response.status_code, 404)

    def test_get_all_users(self):
        self.authenticate(self.user)
        User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword1232',
            first_name='Test2',
            last_name='User2',
        )
        response = self.client.get(
            reverse('v1:user_list'),
        )
        self.assertEqual(response.status_code, 200)
        users_json = response.json()
        self.assertEqual(len(users_json), 2)

    def test_get_user_returns_correct_fields(self):
        self.authenticate(self.user)
        response = self.client.get(
            reverse('v1:user_detail', kwargs={'public_user_id': self.user.public_user_id}),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertNotIn('password', data)

    def test_get_other_users_profile_returns_404(self):
        other_user = make_user('other', 'other@example.com')
        self.authenticate(self.user)
        response = self.client.get(
            reverse('v1:user_detail', kwargs={'public_user_id': other_user.public_user_id}),
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_other_users_profile_returns_404(self):
        other_user = make_user('other', 'other@example.com')
        self.authenticate(self.user)
        response = self.client.delete(
            reverse('v1:user_detail', kwargs={'public_user_id': other_user.public_user_id}),
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(User.objects.filter(public_user_id=other_user.public_user_id).exists())

    def test_unauthenticated_get_user_returns_401(self):
        response = self.client.get(
            reverse('v1:user_detail', kwargs={'public_user_id': self.user.public_user_id}),
        )
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_delete_user_returns_401(self):
        response = self.client.delete(
            reverse('v1:user_detail', kwargs={'public_user_id': self.user.public_user_id}),
        )
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_user_list_returns_401(self):
        response = self.client.get(reverse('v1:user_list'))
        self.assertEqual(response.status_code, 401)

class RegisterTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_creates_user_and_returns_tokens(self):
        payload = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'password': 'StrongPass123!',
        }
        response = self.client.post(reverse('v1:register'), data=payload, format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)
        self.assertTrue(User.objects.filter(email='alice@example.com').exists())

    def test_register_duplicate_email_returns_400(self):
        make_user('alice', 'alice@example.com')
        payload = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'password': 'StrongPass123!',
        }
        response = self.client.post(reverse('v1:register'), data=payload, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_missing_required_fields_returns_400(self):
        response = self.client.post(
            reverse('v1:register'),
            data={'email': 'alice@example.com'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_register_returns_user_data_in_response(self):
        payload = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'password': 'StrongPass123!',
        }
        response = self.client.post(reverse('v1:register'), data=payload, format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('user', data)
        self.assertIn('public_user_id', data['user'])
        self.assertNotIn('password', data['user'])
        self.assertEqual(data['user']['username'], 'alice@example.com')

    def test_register_email_normalized_to_lowercase(self):
        payload = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'Alice@Example.COM',
            'password': 'StrongPass123!',
        }
        response = self.client.post(reverse('v1:register'), data=payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email='alice@example.com').exists())

    def test_register_weak_password_returns_400(self):
        payload = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'password': 'password',
        }
        response = self.client.post(reverse('v1:register'), data=payload, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_email_format_returns_400(self):
        payload = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'not-an-email',
            'password': 'StrongPass123!',
        }
        response = self.client.post(reverse('v1:register'), data=payload, format='json')
        self.assertEqual(response.status_code, 400)

class JWTAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_authenticate_user(self):
        payload = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'password': 'StrongPass123!',
        }
        response = self.client.post(reverse('v1:register'), data=payload, format='json')
        self.assertEqual(response.status_code, 201)

        user_data = {
            "email": "alice@example.com",
            "password": "StrongPass123!",
        }
        response = self.client.post(reverse('v1:token_obtain_pair'), data=user_data, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

    def test_authenticate_wrong_password_returns_401(self):
        make_user('alice', 'alice@example.com')
        response = self.client.post(
            reverse('v1:token_obtain_pair'),
            data={'email': 'alice@example.com', 'password': 'WrongPassword!'},
            format='json',
        )
        self.assertEqual(response.status_code, 401)

    def test_authenticate_nonexistent_user_returns_401(self):
        response = self.client.post(
            reverse('v1:token_obtain_pair'),
            data={'email': 'nobody@example.com', 'password': 'StrongPass123!'},
            format='json',
        )
        self.assertEqual(response.status_code, 401)

    def test_refresh_token_returns_new_access_token(self):
        user = make_user('alice', 'alice@example.com')
        refresh = RefreshToken.for_user(user)
        response = self.client.post(
            reverse('v1:token_refresh'),
            data={'refresh': str(refresh)},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())

    def test_invalid_token_on_protected_endpoint_returns_401(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer notavalidtoken')
        response = self.client.get(reverse('v1:user_list'))
        self.assertEqual(response.status_code, 401)


# class CameraTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = make_user('alice', 'alice@example.com', first_name='Alice', last_name='Smith')
#         self.other_user = make_user('bob', 'bob@example.com', first_name='Bob', last_name='Jones')
#         self.client.force_authenticate(user=self.user)
#         self.camera = Camera.objects.create(owner=self.user, location='Front door')
#
#     def test_list_cameras_returns_only_owned(self):
#         Camera.objects.create(owner=self.other_user, location='Garage')
#         response = self.client.get(reverse('v1:camera-list'))
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(len(data), 1)
#         self.assertEqual(data[0]['location'], 'Front door')
#
#     def test_create_camera_returns_201_and_persists(self):
#         payload = {'location': 'Back yard'}
#         response = self.client.post(reverse('v1:camera-list'), data=payload, format='json')
#         self.assertEqual(response.status_code, 201)
#         self.assertTrue(Camera.objects.filter(location='Back yard', owner=self.user).exists())
#
#     def test_create_camera_missing_required_fields_returns_400(self):
#         response = self.client.post(reverse('v1:camera-list'), data={}, format='json')
#         self.assertEqual(response.status_code, 400)
#
#     def test_get_camera_returns_correct_data(self):
#         response = self.client.get(
#             reverse('v1:camera-detail', kwargs={'public_camera_id': self.camera.public_camera_id})
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['location'], 'Front door')
#
#     def test_get_other_users_camera_returns_404(self):
#         other_camera = Camera.objects.create(owner=self.other_user, location='Garage')
#         response = self.client.get(
#             reverse('v1:camera-detail', kwargs={'public_camera_id': other_camera.public_camera_id})
#         )
#         self.assertEqual(response.status_code, 404)
#
#     def test_update_camera_location(self):
#         response = self.client.patch(
#             reverse('v1:camera-detail', kwargs={'public_camera_id': self.camera.public_camera_id}),
#             data={'location': 'Side gate'},
#             format='json',
#         )
#         self.assertEqual(response.status_code, 200)
#         self.camera.refresh_from_db()
#         self.assertEqual(self.camera.location, 'Side gate')
#
#     def test_delete_camera_returns_204_and_removes_record(self):
#         response = self.client.delete(
#             reverse('v1:camera-detail', kwargs={'public_camera_id': self.camera.public_camera_id})
#         )
#         self.assertEqual(response.status_code, 204)
#         self.assertFalse(Camera.objects.filter(pk=self.camera.pk).exists())
#
#     def test_unauthenticated_access_returns_401(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.get(reverse('v1:camera-list'))
#         self.assertEqual(response.status_code, 401)
#
#
# class RuleTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = make_user('alice', 'alice@example.com', first_name='Alice', last_name='Smith')
#         self.other_user = make_user('bob', 'bob@example.com', first_name='Bob', last_name='Jones')
#         self.client.force_authenticate(user=self.user)
#         self.camera = Camera.objects.create(owner=self.user, location='Front door')
#         self.rule = Rule.objects.create(
#             owner=self.user,
#             camera=self.camera,
#             rule='Notify on motion',
#             rule_nickname='Motion alert',
#         )
#
#     def _rules_list_url(self, camera=None):
#         camera = camera or self.camera
#         return reverse('v1:camera-rules-list', kwargs={
#             'parent_lookup_public_camera_id': camera.public_camera_id,
#         })
#
#     def _rule_detail_url(self, rule=None, camera=None):
#         rule = rule or self.rule
#         camera = camera or self.camera
#         return reverse('v1:camera-rules-detail', kwargs={
#             'parent_lookup_public_camera_id': camera.public_camera_id,
#             'public_rule_id': rule.public_rule_id,
#         })
#
#     def test_list_rules_returns_only_camera_rules(self):
#         other_camera = Camera.objects.create(owner=self.user, location='Garage')
#         Rule.objects.create(owner=self.user, camera=other_camera, rule='Other rule', rule_nickname='Other')
#         response = self.client.get(self._rules_list_url())
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(len(data), 1)
#         self.assertEqual(data[0]['rule'], 'Notify on motion')
#
#     def test_create_rule_returns_201_and_persists(self):
#         payload = {'rule': 'Notify on sound', 'rule_nickname': 'Sound alert'}
#         response = self.client.post(self._rules_list_url(), data=payload, format='json')
#         self.assertEqual(response.status_code, 201)
#         self.assertTrue(Rule.objects.filter(rule='Notify on sound', camera=self.camera).exists())
#
#     def test_create_rule_missing_required_fields_returns_400(self):
#         response = self.client.post(
#             self._rules_list_url(),
#             data={'rule': 'Notify on sound'},
#             format='json',
#         )
#         self.assertEqual(response.status_code, 400)
#
#     def test_get_rule_returns_correct_data(self):
#         response = self.client.get(self._rule_detail_url())
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(data['rule'], 'Notify on motion')
#         self.assertEqual(data['rule_nickname'], 'Motion alert')
#
#     def test_update_rule_nickname(self):
#         response = self.client.patch(
#             self._rule_detail_url(),
#             data={'rule_nickname': 'Updated alert'},
#             format='json',
#         )
#         self.assertEqual(response.status_code, 200)
#         self.rule.refresh_from_db()
#         self.assertEqual(self.rule.rule_nickname, 'Updated alert')
#
#     def test_delete_rule_returns_204_and_removes_record(self):
#         response = self.client.delete(self._rule_detail_url())
#         self.assertEqual(response.status_code, 204)
#         self.assertFalse(Rule.objects.filter(pk=self.rule.pk).exists())
#
#     def test_access_rules_on_other_users_camera_returns_403(self):
#         other_camera = Camera.objects.create(owner=self.other_user, location='Garage')
#         response = self.client.get(self._rules_list_url(camera=other_camera))
#         self.assertEqual(response.status_code, 403)
#
#     def test_unauthenticated_access_returns_401(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.get(self._rules_list_url())
#         self.assertEqual(response.status_code, 401)
