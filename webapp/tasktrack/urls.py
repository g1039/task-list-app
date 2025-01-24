"""Expose the application url config."""

from django.urls import path

from webapp.tasktrack.views import home_view

urlpatterns = [
    path("", home_view, name="home"),
]
