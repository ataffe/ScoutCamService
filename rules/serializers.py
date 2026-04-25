from rest_framework import serializers
from rules.models import Rule

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        read_only_fields = ['public_rule_id', 'owner', 'camera', 'created_at']