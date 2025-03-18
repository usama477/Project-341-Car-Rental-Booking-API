"""Serializers for the todos application"""
from rest_framework import serializers
from .models import Task, CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True)

    class Meta:
        """Meta options for UserRegistrationSerializer"""
        model = CustomUser
        fields = ('email', 'name', 'password')

    def create(self, validated_data):
        """Create and return a new user"""
        return CustomUser.objects.create_user(**validated_data)

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task model"""
    class Meta:
        """Meta options for TaskSerializer"""
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        """Create and return a new task"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
