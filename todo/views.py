from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Project
from django.views import View
from django.views.generic import DetailView, ListView,UpdateView
from .forms import ProjectForm
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
    template_name = 'todo/project_detail.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(id=self.kwargs['pk'])
        projects = Project.objects.filter(user_id=user_id).prefetch_related('tasks')
        context['project'] = project
        context['object_list']=projects
        p_def = self.get_projects_context(self.request)
        return dict(list(context.items())+list(p_def.items()))

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            project = self.get_object()
            print(request.user.id)
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
    
    