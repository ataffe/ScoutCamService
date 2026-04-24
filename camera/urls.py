from rest_framework_nested import routers

from camera.views import CameraViewSet

app_name = 'camera'

camera_router = routers.DefaultRouter()
camera_router.register(r'cameras', CameraViewSet, basename='camera')

urlpatterns = [
    *camera_router.urls,
]