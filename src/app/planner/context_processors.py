from app.planner.models import TaskModel, TaskStatus


def global_stats(request):
    if not request.user.is_authenticated:
        return {'global_total': 0, 'global_done': 0}
    tasks = TaskModel.objects.filter(
        tasklist__user=request.user,
        tasklist__archived=False,
    ).exclude(status=TaskStatus.CANCELED)
    return {
        'global_total': tasks.count(),
        'global_done': tasks.filter(status=TaskStatus.DONE).count(),
    }
