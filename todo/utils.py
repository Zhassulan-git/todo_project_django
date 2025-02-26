from .models import Project, Task
from .forms import ProjectForm

class DataMixin:
    #get all projects for particular user
    def get_projects_context(self, request, **kwargs):
        context = kwargs
        tasks = Project.objects.filter(user_id=request.user).prefetch_related('tasks')
        context['project_with_tasks'] = tasks
        return context