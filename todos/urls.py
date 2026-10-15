from django.urls import path
from . import views
app_name = "todos"
urlpatterns = [
    path("", views.todo_list, name="list"),
    path("todos/new/", views.todo_create, name="create"),
    path("todos/<int:pk>/edit/", views.todo_update, name="update"),
    path("todos/<int:pk>/delete/", views.todo_delete, name="delete"),
    path("todos/<int:pk>/toggle/", views.todo_toggle, name="toggle"),
]
