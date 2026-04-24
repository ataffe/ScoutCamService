from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import RegisterUserSerializer, UserSerializer


class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user)

        return JsonResponse({
            'user': {
                'public_user_id': str(user.public_user_id),
                'username': user.email,
            },
            'access': str(token.access_token),
            'refresh': str(token),
        }, status=status.HTTP_201_CREATED)

class UserView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    lookup_field = 'public_user_id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(public_user_id=self.request.user.public_user_id)

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()[:25]
    permission_classes = [permissions.IsAuthenticated]
