"""Expose the application url config."""

from django.urls import path

from webapp.tasktrack.views import (
    create_task,
    create_task_view,
    dashboard_view,
    delete_calendar_task,
    delete_task_view,
    home_view,
    task_calendar_api,
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
    path("api/tasks/", task_calendar_api, name="task_calendar_api"),
    path("calendar/", create_task, name="calendar"),
    path(
        "delete-calendar-task/<int:task_id>/",
        delete_calendar_task,
        name="delete_calendar_task",
    ),
]
