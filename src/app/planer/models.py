from enum import IntEnum, auto

from django.db import models
from django.contrib.auth.models import User


class TaskStatus(IntEnum):
    PENDING = auto()
    DONE = auto()
    CANCELED = auto()

    @classmethod
    def choices(cls):
        return (
            ('PENDING', cls.PENDING),
            ('DONE', cls.DONE),
            ('CANCELED', cls.CANCELED),
        )



class Tasklist(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    progress = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, default=None, blank=True)
    end_date = models.DateField(null=True, default=None, blank=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(null=True, default=None, blank=True)
    end_date = models.DateField(null=True, default=None, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=TaskStatus.choices(), default=TaskStatus.PENDING)
    deadline = models.DateField(null=True, default=None, blank=True)
    tasklist = models.ForeignKey(Tasklist, on_delete=models.CASCADE)

    def __str__(self):
        return self.name