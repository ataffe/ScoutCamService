from django.shortcuts import render
from django.http import JsonResponse, Http404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rules.models import User, Camera, Rule
from rules.serializers import UserSerializer, RuleSerializer, CameraSerializer

class UserDetail(APIView):
    """
    Retrieve, update or delete a User instance.
    """

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_user(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(APIView):
    """
    List all users.
    """
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

class RuleDetail(APIView):
    """
    Retrieve, update or delete a Rule instance.
    """
    def get_rule(self, pk):
        try:
            return Rule.objects.get(pk=pk)
        except Rule.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        rule = self.get_rule(pk)
        serializer = RuleSerializer(rule)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = RuleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        rule = self.get_rule(pk)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RuleList(APIView):
    """
    Retrieve a list of rules for a user.
    """
    def get(self, request, user_id):
        rules = Rule.objects.filter(user_id=user_id)
        serializer = RuleSerializer(rules, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class CameraDetail(APIView):
    """
    Retrieve, update or delete a Camera instance.
    """
    def get_camera(self, pk):
        try:
            return Camera.objects.get(pk=pk)
        except Camera.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        camera = self.get_camera(pk)
        serializer = CameraSerializer(camera)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CameraSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        camera = self.get_camera(pk)
        camera.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CameraList(APIView):
    """
    Retrieve a list of cameras.
    """
    def get(self, request, user_id):
        cameras = Camera.objects.filter(user_id=user_id)
        serializer = CameraSerializer(cameras, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
