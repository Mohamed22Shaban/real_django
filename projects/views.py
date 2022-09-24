from asyncio import Task
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

# Create your views here.
from django.views.generic import ListView, CreateView ,UpdateView, DeleteView
from . models import Project ,Task
from .forms import ProjectCreateForm ,ProjectupdateForm

## 2)

class ProjectListView(ListView):
    model = Project                  #= define the class
    template_name = 'project/list.html'
    #add pagination
    paginate_by = 3

    def get_queryset(self):  #> to get the search word in the page list
        query_set = super().get_queryset()
        where  = {}# > include the request terms
        q = self.request.GET.get('q',None) #=> ensure if the word 'q' are exist
        if q:where['title_icontains'] = q
        return query_set.filter(**where)


## 4) create class to add forms to it

class ProjectCreateView(CreateView):
    model = Project                 
    form_class = ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('project_list') # project list => the name exist in urlapp

## 6) create class to update forms to it
## 7) and make linke to it with the list page

class ProjectupdateView(UpdateView):
    model = Project                 
    form_class = ProjectupdateForm
    template_name = 'project/update.html'
    success_url = reverse_lazy('project_list') # project list => the name exist in urlapp

     # if you would stay in the update page not move to the project_list
    # def get_success_url(self):
    #     return reverse('project_update',args=[self.object.id])  =>>>> args=[self.object_id] => to the id one task
    



## 8) deal with create task without create form  ,, and create template to it and include task.html in update.html

class TaskCreateView(CreateView):
    model = Task               
    fields = ['project','description']    
    http_method_names = ['post']    # => to stop the creat page and make this class just for store the tasks
    def get_success_url(self):
        return reverse('project_update',args=[self.object.project.id]) 



## 8) deal with update task without update form  ,,and add it to task.html

class TaskUpdateView(UpdateView):
    model = Task               
    fields = ['is_completed']    
    http_method_names = ['post']  
    def get_success_url(self):
        return reverse('project_update',args=[self.object.project.id]) 


## 8) deal with delete task without create form  ,, and add it to task.html
class TaskDeleteView(DeleteView):
    model = Task                  
    def get_success_url(self):
        return reverse('project_update',args=[self.object.project.id]) 




## 8) deal with delete the whole project ,, and add url it to update.html
class ProjectDeleteView(DeleteView):
    model = Project
    template_name ='project/delete.html'   
    success_url = reverse_lazy('project_list')               



##  9) create template to print fields and error   during bootstrap