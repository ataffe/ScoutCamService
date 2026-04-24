from rest_framework import serializers

from camera.models import Camera

class CameraSerializer(serializers.ModelSerializer):
    public_camera_id = serializers.UUIDField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Camera
        fields = '__all__'
        read_only_fields = ['public_camera_id', 'owner', 'created_at']