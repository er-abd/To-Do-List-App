from django.contrib import admin
# that is how we import a model we created.
from .models import Task
# Register your models here.


# now we regiter a model we created
admin.site.register(Task)
