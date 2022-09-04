from re import T
from django.db import models
# this is a built-in Djngo table that deals with users and user authentication. -> it is used in the class named Task.
from django.contrib.auth.models import User
# Create your models here.


# models.Model is an inheretance to make it a model.


class Task(models.Model):
    # one user can have many tasks. (1-many)
    # balnk is for the form and null is for the DB.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    # unlike CharField, TextField gives us a box.
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    # automatically assign a date and time stamp when it is created.
    created = models.DateTimeField(auto_now_add=True)

    # that is how we set the defult value to title.

    def __str__(self):
        return self.title

    # this class makes some changes to the original model "Task"
    class Meta:
        # the order when we return multiple items.
        ordering = ["complete"]
