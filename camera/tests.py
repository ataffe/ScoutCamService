from django.test import TestCase

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
