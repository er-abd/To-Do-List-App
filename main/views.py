from asyncio import Task
from contextlib import redirect_stderr
from distutils.log import Log
from multiprocessing import context
from re import U
from typing import List
from urllib import request
from django.shortcuts import render, redirect
# this to use class-based views
from django.views.generic.list import ListView
# this is to show the details of every item in a list (READ)
from django.views.generic.detail import DetailView
# this is for CRUD functionality.
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# this is used to redirect our user to another page when create/edit/delete is completed.
from django.urls import reverse_lazy
# this is for the built-in login form
from django.contrib.auth.views import LoginView
# this used to restrict unauthenticated users from accessing some pages.
from django.contrib.auth.mixins import LoginRequiredMixin
#
from django.contrib.auth.forms import UserCreationForm
# to log the user in directly after they create an account
from django.contrib.auth import login
# every model created must ne linked to the views as below.
from .models import Task


# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    # the model is already built we just need to use the fields.
    fields = '__all__'
    # once a user attempts to reach the page, they will be redirected.
    redirect_authenticated_user = True

    # this is just like success_url = reverse_lazy('tasks')
    def get_success_url(self):
        return reverse_lazy('tasks')


# to create a register view
class RegisterPage(FormView):
    template_name = 'main/register.html'
    # we are using the django user built in user registeration form.
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    # here we redirect the user when the form is submitted.
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


# when using LoginRequiredMixin, do not to edit the defult settings in settings.py
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    # this will be used to render the data in for loops in the template (This is a costomization instead of object_list)
    # now this view will lok for a template starts with the word "task" (which is the model name) THEN  _list.html.    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # request.user is used in the template. This tells django to only output the tasks of the logged in user.
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        # this is used to show the number of incomplete items. It takes the filtered data from the line above ^ then it applies another filter and count the number of filterred data.
        context['count'] = context['tasks'].filter(complete=False).count()

        # here we deal with the search functionality
        # get the 'saerch_area' from the search_input GET mwthod if nothing in it then it is empty.
        search_input = self.request.GET.get("search-area".lower) or ''
        # here we decide how we filter the data we get and how we use to search.
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)

        context['search_input'] = search_input

        return context


# this view returns info about a single item.
class TaskDetail(LoginRequiredMixin, DetailView):
    # this is the model we aree using (Where we get the data for this view from.)
    # now this view will lok for a template starts with the word "task" (which is the model name) THEN  _detail.html.
    model = Task
    # that is to customize the defult object variable that we use in e.g. loops in the template. (WE want to render it by that given name)
    context_object_name = 'task'
    # that is to customize the defult template that django will look for (Which is modelname_detail) and tell the view which template to look for.
    template_name = 'main/task.html'


class TaskCraete(LoginRequiredMixin, CreateView):
    model = Task
    # by defult the create view gives us a model form. (Fields for all things in the model Task in models.py)
    # here we specify the fields we want to show (all fields)
    fields = ['title', 'description', 'complete']
    # if an item is created successfully, redirect the user to the page with url named tasks.
    success_url = reverse_lazy('tasks')

    # This method is alraedy built-in and we can simply use it but we need to overwrite it first (modify it)
    # this method will allow the user to only add notes to their account and not others.
    def form_valid(self, form):
        # request.user means the user who requested the order (the logged in user).
        form.instance.user = self.request.user
        return super(TaskCraete, self).form_valid(form)


# UpdateView pre-fills the form and when something is edited it updates it.
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
