from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    # Must be using PostgreSQL 18+ for the native UUID7 support.
    # public_user_id = models.UUIDField(editable=False, unique=True, db_default=models.Func(function="uuidv7"))
    public_user_id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

class Camera(models.Model):
    id = models.BigAutoField(primary_key=True)
    # Must be using PostgreSQL 18+ for the native UUID7 support.
    # public_camera_id = models.UUIDField(editable=False, unique=True, db_default=models.Func(function="uuidv7"))
    public_camera_id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Camera at location {self.location} for user {self.owner.id}.'

class Rule(models.Model):
    id = models.BigAutoField(primary_key=True)
    # Must be using PostgreSQL 18+ for the native UUID7 support.
    # public_rule_id = models.UUIDField(editable=False, unique=True, db_default=models.Func(function="uuidv7"))
    public_rule_id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    rule = models.CharField(max_length=240)
    rule_nickname = models.CharField(max_length=240)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Rule: "{self.rule_nickname}" for user {self.owner.id} on camera {self.camera_id}.'
