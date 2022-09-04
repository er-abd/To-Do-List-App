from django.urls import path
from .views import CustomLoginView, TaskDelete, TaskList, TaskDetail, TaskCraete, TaskUpdate, UpdateView, DeleteView, RegisterPage
from django.contrib.auth.views import LogoutView

# here we add urls for the views that we have created.
# '' means the main/root url // name is the name of our url
# do not forget to regist these urls (of this specific app) in urls.py in the project's root dir.
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    # after they finish with this page we send the user to teh login page
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    # as_view() method tregars the fuction type inside the view (POST or GET).
    path('', TaskList.as_view(), name='tasks'),
    # pk is specific for each item
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCraete.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
]
