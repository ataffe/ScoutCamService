from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserListView, RegisterUserView, UserView

app_name = 'users'

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<uuid:public_user_id>/', UserView.as_view(), name='user_detail'),
    path('users/', UserListView.as_view(), name='user_list'),
]