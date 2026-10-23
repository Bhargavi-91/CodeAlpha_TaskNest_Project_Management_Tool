from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProjectForm, TaskForm
from .models import Project, Task

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request, "tasks/register.html", {"form": form})

@login_required
def task_list(request):
    projects = Project.objects.filter(owner=request.user).prefetch_related("tasks")
    status_filter = request.GET.get("status", "")
    tasks = Task.objects.filter(project__owner=request.user).select_related("project")
    if status_filter in {"TODO", "IN_PROGRESS", "DONE"}:
        tasks = tasks.filter(status=status_filter)
    counts = {
        "total": Task.objects.filter(project__owner=request.user).count(),
        "todo": Task.objects.filter(project__owner=request.user, status="TODO").count(),
        "progress": Task.objects.filter(project__owner=request.user, status="IN_PROGRESS").count(),
        "done": Task.objects.filter(project__owner=request.user, status="DONE").count(),
    }
    return render(request, "tasks/task_list.html", {
        "projects": projects, "tasks": tasks, "counts": counts, "status_filter": status_filter
    })

@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, "Project created.")
            return redirect("task_list")
    else:
        form = ProjectForm()
    return render(request, "tasks/project_form.html", {"form": form, "heading": "Create a project"})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    tasks = project.tasks.all()
    return render(request, "tasks/project_detail.html", {"project": project, "tasks": tasks})

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, "Task created.")
            return redirect("project_detail", project_id=project.id)
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form, "heading": "Add a task", "project": project})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id, project__owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated.")
            return redirect("project_detail", project_id=task.project_id)
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "heading": "Edit task", "project": task.project})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, project__owner=request.user)
    project_id = task.project_id
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted.")
    return redirect("project_detail", project_id=project_id)
