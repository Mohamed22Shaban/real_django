from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import ListView, CreateView
from . models import Project
from .forms import ProjectCreateForm

## 2)

class ProjectListView(ListView):
    model = Project                  #= define the class
    template_name = 'project/list.html'
    queryset = Project.objects.all()



## 4) create class to add forms to it

class ProjectCreateView(CreateView):
    model = Project                 
    form_class = ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('project_list') # project list => the name exist in urlapp

