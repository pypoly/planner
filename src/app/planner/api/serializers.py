from rest_framework import serializers

from app.planner.models import TaskModel, ToDoListModel, TaskStatus


class TaskSerializer(serializers.ModelSerializer):
    tasklist = serializers.PrimaryKeyRelatedField(queryset=ToDoListModel.objects.filter(archived=False))

    class Meta:
        model = TaskModel
        fields = '__all__'



