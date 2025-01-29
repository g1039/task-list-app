"""Expose the application url config."""

from django.urls import path

from webapp.tasktrack.views import (
    create_task_view,
    dashboard_view,
    delete_task_view,
    home_view,
    task_details_view,
    task_update_view,
    task_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("dashboard", dashboard_view, name="dashboard"),
    path("tasks-list/", task_view, name="tasks"),
    path("create-task/", create_task_view, name="create_task"),
    path("task-details/ <int:pk>/", task_details_view, name="task_details"),
    path("task-update/ <int:pk>/", task_update_view, name="task_update"),
    path("delete-task/<int:pk>", delete_task_view, name="delete_task"),
]
