from enum import IntEnum, auto

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class TaskStatus(IntEnum):
    PENDING = auto()
    DONE = auto()
    CANCELED = auto()

    @classmethod
    def choices(cls):
        return (
            (cls.PENDING, 'PENDING'),
            (cls.DONE, 'DONE'),
            (cls.CANCELED, 'CANCELED'),
        )


class ToDoItemQuerySet(models.QuerySet):
    def active(self):
        return self.filter(archived=False)

    def done(self):
        return self.filter(archived=True)


class ToDoListModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    progress = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, default=None, blank=True)
    end_date = models.DateField(null=True, default=None, blank=True)
    archived = models.BooleanField(default=False)

    objects = ToDoItemQuerySet.as_manager()

    def __str__(self):
        return self.title


class TaskModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, default=None, blank=True)
    end_date = models.DateField(null=True, default=None, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=TaskStatus.choices(), default=TaskStatus.PENDING)
    deadline = models.DateField(null=True, default=None, blank=True)
    tasklist = models.ForeignKey(ToDoListModel, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.name


@receiver(post_save, sender=TaskModel)
def update_progress(sender, instance, created, **kwargs):
    all_tasks: list[TaskModel] = TaskModel.objects.filter(
        tasklist=instance.tasklist).exclude(status=TaskStatus.CANCELED)
    total_count = len(all_tasks)
    if total_count > 0:
        done_count = len([x for x in all_tasks if x.status == TaskStatus.DONE])
        progress = int((done_count / total_count)*100)
    else:
        progress = 0
    ToDoListModel.objects.filter(pk=instance.tasklist.pk).update(progress=progress)
