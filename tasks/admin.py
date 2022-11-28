from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin): #ver los que son solo lectura
    readonly_fields = ("created", )

# Register your models here.
admin.site.register(Task, TaskAdmin) # Admin crear tareas habilitado