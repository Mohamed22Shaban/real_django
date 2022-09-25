from asyncio import Task
import django
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

# Create your views here.
from django.views.generic import ListView, CreateView ,UpdateView, DeleteView 
from . models import Project ,Task
from .forms import ProjectCreateForm ,ProjectupdateForm
## 11) protect the show page for just user
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin

## 2)

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project                                  #= define the class
    template_name = 'project/list.html'
    paginate_by = 3

    #> to get the search word in the page list
    def get_queryset(self):
        query_set = super().get_queryset()
        where = {'user_id': self.request.user}  # > include the request terms  ,,,,{'user_id':self.request.user} =>and put in it the protect standard
        q = self.request.GET.get('q', None)       #=> ensure if the word 'q' are exist
        if q:
            where['title__icontains'] = q
        return query_set.filter(**where)



## 4) create class to add forms to it

class ProjectCreateView(CreateView, LoginRequiredMixin):
    model = Project                 
    form_class = ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('project_list') # project list => the name exist in urlapp

    # define user id and save it
    def form_valid(self, form):
        form.instance.user = self.request.user  #= So when save project the user will save also
        return super().form_valid(form)

## 6) create class to update forms to it
## 7) and make linke to it with the list page

class ProjectupdateView(UpdateView, UserPassesTestMixin,LoginRequiredMixin):    #=. to protect the project from external update
    model = Project                 
    form_class = ProjectupdateForm
    template_name = 'project/update.html'
    # success_url = reverse_lazy('project_list') # project list => the name exist in urlapp

     # if you would stay in the update page not move to the project_list
    def get_success_url(self):
        return reverse('project_update',args=[self.object.id])  #=>>>> args=[self.object_id] => to the id one task
    
    ## to protect 
    def test_func(self) :
        return self.get_object().user_id == self.request.user.id



## 8) deal with create task without create form  ,, and create template to it and include task.html in update.html

class TaskCreateView(CreateView, UserPassesTestMixin,LoginRequiredMixin):
    model = Task               
    fields = ['project','description']    
    http_method_names = ['post']    # => to stop the creat page and make this class just for store the tasks
    def get_success_url(self):
        return reverse('project_update',args=[self.object.project.id]) 

    # to protect and ensure the user who create task
    def test_func(self):
        project_id = self.request.POST.get('project', '')
        return Project.objects.get(pk=project_id).user_id == self.request.user.id



## 8) deal with update task without update form  ,,and add it to task.html

class TaskUpdateView(UpdateView,UserPassesTestMixin, LoginRequiredMixin):
    model = Task               
    fields = ['is_completed']    
    http_method_names = ['post']  
    def get_success_url(self):
        return reverse('project_update',args=[self.object.project.id]) 

    ## to protect 
    def test_func(self) :
        return self.get_object().project.user_id == self.request.user.id


## 8) deal with delete task without create form  ,, and add it to task.html
class TaskDeleteView(DeleteView,UserPassesTestMixin , LoginRequiredMixin):
    model = Task                  
    def get_success_url(self):
        return reverse('project_update',args=[self.object.project.id]) 
    ## to protect 
    def test_func(self) :
        return self.get_object().project.user_id == self.request.user.id





## 9) deal with delete the whole project ,, and add url it to update.html
class ProjectDeleteView(DeleteView,UserPassesTestMixin, LoginRequiredMixin):
    model = Project
    template_name ='project/delete.html'   
    success_url = reverse_lazy('project_list')               

    # to protect
    def test_func(self) :
        return self.get_object().user_id == self.request.user.id


##  10) create template to print fields and error   during bootstrap