from django.contrib import messages
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import TodoForm
from .models import Todo


def todo_list(request):
    return render(request, "todos/list.html", {"todos": Todo.objects.all()})


def todo_create(request):
    form = TodoForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "할 일을 등록했습니다.")
        return redirect("todos:list")
    return render(request, "todos/form.html", {"form": form, "heading": "새 할 일 등록"})


def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    form = TodoForm(request.POST if request.method == "POST" else None, instance=todo)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "할 일을 수정했습니다.")
        return redirect("todos:list")
    return render(request, "todos/form.html", {"form": form, "heading": "할 일 수정"})


def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        todo.delete()
        messages.success(request, "할 일을 삭제했습니다.")
        return redirect("todos:list")
    return render(request, "todos/confirm_delete.html", {"todo": todo})


@require_POST
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    Todo.objects.filter(pk=todo.pk).update(is_completed=~F("is_completed"))
    return redirect("todos:list")
