from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rules.models import User, Camera, Rule

class UserSerializer(serializers.ModelSerializer):
    public_user_id = serializers.UUIDField(read_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'public_user_id']

class CameraSerializer(serializers.ModelSerializer):
    public_camera_id = serializers.UUIDField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Camera
        fields = '__all__'
        read_only_fields = ['public_camera_id', 'owner', 'location', 'created_at']

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        read_only_fields = ['public_rule_id', 'camera', 'rule', 'rule_nickname', 'is_enabled', 'created_at']

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with that email already exists.')
        return value.lower()

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

