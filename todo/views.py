from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .models import Project, Task
from django.views import View
from django.views.generic import DetailView, ListView,UpdateView, CreateView, DeleteView
from .forms import ProjectForm, TaskForm
from django.contrib import messages
from .utils import DataMixin

class Home(DataMixin, ListView):
    model = Project
    template_name = 'todo/home.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        p_def = self.get_projects_context(self.request, title='Main page')
        return dict(list(context.items())+list(p_def.items()))

class ProjectDetailView(DataMixin, DetailView):
    model = Project
    form_class = TaskForm
    template_name = 'todo/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_def = self.get_projects_context(self.request)
        return dict(list(context.items())+list(p_def.items()))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        project = get_object_or_404(Project, pk=kwargs.get('pk'))
        if 'delete' in request.POST:
            if project.user_id == request.user.id:
                project.delete()
                return redirect('home')
        return self.get(request, *args, **kwargs)



class ProjectCreateView(DataMixin, ListView):
    model = Project
    template_name = 'todo/create_project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ProjectForm()
        context['form'] = form
        p_def = self.get_projects_context(self.request, title='Create a new project')
        return dict(list(context.items())+list(p_def.items()))
    

    def post(self, request):  
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = request.user.id
            form.save()
            return redirect('home') 
        return render(request, self.template_name, {'form':form})

    

class ProjectUpdateView(DataMixin, UpdateView):
    template_name = 'todo/update_project.html'
    model = Project
    fields = ['title', 'description']
    def get_success_url(self):
        return reverse_lazy('detail-project', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        form = ProjectForm()
        project_item = Project.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['form'] = form
        context['project'] = project_item
        p_def = self.get_projects_context(self.request, title=project_item.title)
        return dict(list(context.items())+list(p_def.items()))
    

class TaskUpdateView(DataMixin, UpdateView):
    model=Task
    form_class = TaskForm
    template_name = 'todo/update_task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_def = self.get_projects_context(self.request)
        return dict(list(context.items())+list(p_def.items()))

    def get_object(self, queryset=None):
        return Task.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        project_id = self.kwargs.get('project_pk')
        return reverse('detail-project', kwargs={'pk': project_id})

class CreateTaskView(DataMixin, CreateView):
    model =Task
    form_class = TaskForm
    template_name = 'todo/add_task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_def = self.get_projects_context(self.request)
        return dict(list(context.items())+list(p_def.items()))
    
    def form_valid(self, form):
        project = Project.objects.get(id=self.kwargs['pk'])
        form.instance.project = project

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-project', kwargs={'pk': self.kwargs['pk']})


class TaskDeleteView(DataMixin, DeleteView):
    model = Task
    template_name = 'todo/delete_task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_def = self.get_projects_context(self.request)
        return dict(list(context.items())+list(p_def.items()))

    def get_success_url(self):
        project_id = self.kwargs.get('project_pk')
        return reverse('detail-project', kwargs={'pk': project_id})

    def get_object(self, queryset=None):
        return Task.objects.get(pk=self.kwargs['pk'])