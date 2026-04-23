from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers
from rules.views import CameraViewSet, RuleViewSet, RegisterUserView, UserView, UserListView

app_name = 'rules'

camera_router = routers.DefaultRouter()
camera_router.register(r'cameras', CameraViewSet, basename='camera')

rules_router = routers.NestedDefaultRouter(camera_router, r'cameras', lookup='public_camera_id')
rules_router.register(r'rules', RuleViewSet, basename='camera-rules')

urlpatterns = [
    *camera_router.urls,
    *rules_router.urls,
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<uuid:public_user_id>', UserView.as_view(), name='user_detail'),
    path('users/', UserListView.as_view(), name='user_list'),
]