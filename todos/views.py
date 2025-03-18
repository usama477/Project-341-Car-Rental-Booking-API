"""Views for the todos application"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Task
from .serializers import UserRegistrationSerializer, TaskSerializer

class UserRegistrationView(APIView):
    """View for user registration"""
    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST request for user registration"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for handling task operations"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return queryset filtered by current user"""
        return Task.objects.filter(user=self.request.user)
