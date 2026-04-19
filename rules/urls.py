from django.urls import path
from rules import views

app_name = 'rules'
urlpatterns = [
    path('user/', views.UserDetail.as_view(), name='user-detail'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('rule/', views.RuleDetail.as_view(), name='rule-detail'),
    path('rule/<int:pk>', views.RuleDetail.as_view(), name='rule-detail'),
    path('rules/user/<int:user_id>', views.RuleList.as_view(), name='rule-list'),
    path('camera/', views.CameraDetail.as_view(), name='camera-detail'),
    path('camera/<int:pk>', views.CameraDetail.as_view(), name='camera-detail'),
    path('cameras/user/<int:user_id>', views.CameraList.as_view(), name='camera-list')
]