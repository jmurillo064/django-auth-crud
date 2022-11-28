from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method== 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user) #cookie session
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Contraseñas no coinciden'
                })

@login_required #proteger rutas configurar el LOGIN_URL en setting
def tasks(request):
    tareas = Task.objects.filter(user=request.user, datecompleted__isnull=True) #por usuario
    return render(request, 'tasks.html', {
        'tareas': tareas
    })

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('home')

def abrirSesion(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def crearTarea(request):
    if request.method == 'GET':
        return render(request, 'created_task.html',{
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST) #guardar los datos con el formulario
            newTask = form.save(commit=False)
            newTask.user = request.user
            newTask.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'created_task.html',{
            'form': TaskForm,
            'error':'Por favor, ingresa datos válidos'
            })

@login_required
def task_unica(request, task_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Task, pk=task_id, user=request.user) #búsqueda de un dato
        form = TaskForm(instance=tarea)
        return render(request, 'task_unica.html',{
            'tarea':tarea,
            'form':form
        })
    else:
        try:
            tarea = get_object_or_404(Task, pk=task_id, user=request.user) #solo editar las propias
            form = TaskForm(request.POST, instance=tarea)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_unica.html',{
                'tarea':tarea,
                'form':form,
                'error':'Error actualizando tarea'
            })

@login_required
def completarTarea(request, task_id):
    tarea = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        tarea.datecompleted = timezone.now()
        tarea.save()
        return redirect('tasks')

@login_required
def eliminarTarea(request, task_id):
    tarea = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tasks')

@login_required
def taskscomplete(request):
    tareas = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') #por usuario
    return render(request, 'tasks.html', {
        'tareas': tareas
    })

