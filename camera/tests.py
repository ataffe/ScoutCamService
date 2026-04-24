from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User
from camera.models import Camera
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

def make_user(username, email, password='StrongPass123!', first_name='Test', last_name='User'):
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

class CameraTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user('alice', 'alice@example.com', first_name='Alice', last_name='Smith')
        self.other_user = make_user('bob', 'bob@example.com', first_name='Bob', last_name='Jones')
        self.authenticate(user=self.user)
        self.camera = Camera.objects.create(owner=self.user, location='Front door')
    
    def get_jwt_token(self, user):
        """Helper to generate a JWT token for a given user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def authenticate(self, user):
        """Helper to set the JWT token on the client."""
        token = self.get_jwt_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_cameras_returns_only_owned(self):
        Camera.objects.create(owner=self.other_user, location='Garage')
        response = self.client.get(reverse('camera:camera-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['location'], 'Front door')

    def test_create_camera_returns_201_and_persists(self):
        payload = {'location': 'Back yard'}
        response = self.client.post(reverse('camera:camera-list'), data=payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Camera.objects.filter(location='Back yard', owner=self.user).exists())

    def test_create_camera_missing_required_fields_returns_400(self):
        response = self.client.post(reverse('camera:camera-list'), data={}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_camera_returns_correct_data(self):
        response = self.client.get(
            reverse('camera:camera-detail', kwargs={'public_camera_id': self.camera.public_camera_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['location'], 'Front door')

    def test_get_other_users_camera_returns_404(self):
        other_camera = Camera.objects.create(owner=self.other_user, location='Garage')
        response = self.client.get(
            reverse('camera:camera-detail', kwargs={'public_camera_id': other_camera.public_camera_id})
        )
        self.assertEqual(response.status_code, 404)

    def test_update_camera_location(self):
        response = self.client.patch(
            reverse('camera:camera-detail', kwargs={'public_camera_id': self.camera.public_camera_id}),
            data={'location': 'Side gate'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.camera.refresh_from_db()
        self.assertEqual(self.camera.location, 'Side gate')

    def test_delete_camera_returns_204_and_removes_record(self):
        response = self.client.delete(
            reverse('camera:camera-detail', kwargs={'public_camera_id': self.camera.public_camera_id})
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Camera.objects.filter(pk=self.camera.pk).exists())

    def test_unauthenticated_access_returns_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('camera:camera-list'))
        self.assertEqual(response.status_code, 401)

    def test_list_returns_empty_when_user_has_no_cameras(self):
        Camera.objects.filter(owner=self.user).delete()
        response = self.client.get(reverse('camera:camera-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_response_includes_public_camera_id(self):
        payload = {'location': 'Driveway'}
        response = self.client.post(reverse('camera:camera-list'), data=payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('public_camera_id', response.json())

    def test_create_ignores_owner_in_payload(self):
        payload = {'location': 'Lobby', 'owner': self.other_user.pk}
        response = self.client.post(reverse('camera:camera-list'), data=payload, format='json')
        self.assertEqual(response.status_code, 201)
        camera = Camera.objects.get(location='Lobby')
        self.assertEqual(camera.owner, self.user)

    def test_update_other_users_camera_returns_404(self):
        other_camera = Camera.objects.create(owner=self.other_user, location='Garage')
        response = self.client.patch(
            reverse('camera:camera-detail', kwargs={'public_camera_id': other_camera.public_camera_id}),
            data={'location': 'Hacked'},
            format='json',
        )
        self.assertEqual(response.status_code, 404)
        other_camera.refresh_from_db()
        self.assertEqual(other_camera.location, 'Garage')

    def test_delete_other_users_camera_returns_404(self):
        other_camera = Camera.objects.create(owner=self.other_user, location='Garage')
        response = self.client.delete(
            reverse('camera:camera-detail', kwargs={'public_camera_id': other_camera.public_camera_id})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Camera.objects.filter(pk=other_camera.pk).exists())

    def test_location_exceeds_max_length_returns_400(self):
        payload = {'location': 'A' * 101}
        response = self.client.post(reverse('camera:camera-list'), data=payload, format='json')
        self.assertEqual(response.status_code, 400)
