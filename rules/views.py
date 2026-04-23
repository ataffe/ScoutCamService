from django.http import JsonResponse, Http404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from rules.models import User, Camera, Rule
from rules.serializers import RuleSerializer, CameraSerializer, RegisterUserSerializer, UserSerializer
from rest_framework import generics, status, permissions, viewsets, mixins
from rest_framework_simplejwt.tokens import  RefreshToken


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


class RuleViewSet(viewsets.ModelViewSet):
    serializer_class = RuleSerializer
    lookup_field = 'public_rule_id'
    permission_classes = [permissions.IsAuthenticated]

    def get_camera(self):
        camera = Camera.objects.filter(
            public_camera_id=self.kwargs['parent_lookup_public_camera_id'],
            owner=self.request.user
        ).first()

        if camera is None:
            raise PermissionDenied('Camera not found or does not belong to this user')
        return camera

    def get_queryset(self):
        return Rule.objects.filter(camera=self.get_camera())

    def perform_create(self, serializer):
        serializer.save(camera=self.get_camera(), owner=self.request.user)

class CameraViewSet(viewsets.ModelViewSet):
    serializer_class = CameraSerializer
    lookup_field = 'public_camera_id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Camera.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# class RuleDetail(APIView):
#     """
#     Retrieve, update or delete a Rule instance.
#     """
#     def get_rule(self, pk):
#         try:
#             return Rule.objects.get(pk=pk)
#         except Rule.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         rule = self.get_rule(pk)
#         serializer = RuleSerializer(rule)
#         return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         data = JSONParser().parse(request)
#         serializer = RuleSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         rule = self.get_rule(pk)
#         rule.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#
# class UserView(generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'email'
#     lookup_url_kwarg = 'email'
#
# class UserList(generics.ListAPIView):
#     """
#     List all users.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]



# class RuleList(APIView):
#     """
#     Retrieve a list of rules for a user.
#     """
#     def get(self, request, user_id):
#         rules = Rule.objects.filter(user_id=user_id)
#         serializer = RuleSerializer(rules, many=True)
#         return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)




# class CameraDetail(APIView):
#     """
#     Retrieve, update or delete a Camera instance.
#     """
#     def get_camera(self, pk):
#         try:
#             return Camera.objects.get(pk=pk)
#         except Camera.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         camera = self.get_camera(pk)
#         serializer = CameraSerializer(camera)
#         return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         data = JSONParser().parse(request)
#         serializer = CameraSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         camera = self.get_camera(pk)
#         camera.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CameraList(APIView):
#     """
#     Retrieve a list of cameras.
#     """
#     def get(self, request, user_id):
#         cameras = Camera.objects.filter(user_id=user_id)
#         serializer = CameraSerializer(cameras, many=True)
#         return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
