from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.planner.api.serializers import TaskSerializer
from app.planner.models import TaskModel


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = TaskModel.objects.all()
        q = queryset.filter(tasklist__user=self.request.user.pk, tasklist__archived=False)
        return q
