from rest_framework import viewsets

from app.planner.api.serializers import TaskSerializer
from app.planner.models import TaskModel


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = TaskModel.objects.all()
        q = queryset.filter(tasklist__user=self.request.user, tasklist__archived=False)
        return q
