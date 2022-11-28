"""djandocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('taskscompleted/', views.taskscomplete, name='taskscomplete'),
    path('tasks/create/', views.crearTarea, name='crearTarea'),
    path('tasks/<int:task_id>/', views.task_unica, name='task_unica'),
    path('tasks/<int:task_id>/complete', views.completarTarea, name='completarTarea'),
    path('tasks/<int:task_id>/delete', views.eliminarTarea, name='eliminarTarea'),
    path('logout/', views.cerrarSesion, name='logout'),
    path('signin/', views.abrirSesion, name='signin')
]
