from .models import Project
from .forms import ProjectForm

class DataMixin:
    #get all projects for particular user
    def get_projects_context(self,request, **kwargs):
        context = kwargs
        user_id = request.user.id
        projects = Project.objects.filter(user_id=user_id).prefetch_related('tasks')
        context['object_list'] = projects
        return context