"""Contains the application template based views."""

from datetime import datetime
from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from webapp.tasktrack import services
from webapp.tasktrack.enums import StatusType
from webapp.tasktrack.forms import CreateTaskForm, TaskUpdateForm
from webapp.tasktrack.models import Task
from webapp.tasktrack.permissions import limit_access


class HomeView(LoginRequiredMixin, TemplateView):
    """Home page view."""

    template_name = "pages/index.html"

    def get_context_data(self, **kwargs: Any) -> Any:
        """Add context for the view."""

        context = super().get_context_data(**kwargs)

        pending_tasks_count = (
            Task.objects.filter(assigned_to=self.request.user).pending_tasks().count()
        )
        in_progress_tasks_count = (
            Task.objects.filter(assigned_to=self.request.user)
            .in_progress_tasks()
            .count()
        )
        completed_tasks_count = (
            Task.objects.filter(assigned_to=self.request.user).completed_tasks().count()
        )
        cancelled_tasks_count = (
            Task.objects.filter(assigned_to=self.request.user).cancelled_tasks().count()
        )

        task_list = Task.objects.filter(assigned_to=self.request.user).order_by("-pk")

        context["task_counts"] = {
            "pending": pending_tasks_count,
            "in_progress": in_progress_tasks_count,
            "completed": completed_tasks_count,
            "cancelled": cancelled_tasks_count,
        }
        context["task_list"] = task_list

        return context


@method_decorator(limit_access, name="get")
class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard page view."""

    template_name = "pages/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> Any:
        """Add context for the view."""

        context = super().get_context_data(**kwargs)

        current_year = datetime.now().year

        pending_tasks_count = Task.objects.all().pending_tasks().count()
        in_progress_tasks_count = Task.objects.all().in_progress_tasks().count()
        completed_tasks_count = Task.objects.all().completed_tasks().count()
        cancelled_tasks_count = Task.objects.all().cancelled_tasks().count()

        low_priority_tasks_count = Task.objects.all().low_priority_tasks().count()
        medium_priority_tasks_count = Task.objects.all().medium_priority_tasks().count()
        high_priority_tasks_count = Task.objects.all().high_priority_tasks().count()
        critical_priority_tasks_count = (
            Task.objects.all().critical_priority_tasks().count()
        )

        jan_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=1
        ).count()
        feb_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=2
        ).count()
        mar_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=3
        ).count()
        apr_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=4
        ).count()
        may_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=5
        ).count()
        jun_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=6
        ).count()
        jul_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=7
        ).count()
        aug_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=8
        ).count()
        sep_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=9
        ).count()
        oct_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=10
        ).count()
        nov_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=11
        ).count()
        dec_due_tasks_count = Task.objects.filter(
            due_date__year=current_year, due_date__month=12
        ).count()

        jan_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=1,
        ).count()
        feb_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=2,
        ).count()
        mar_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=3,
        ).count()
        apr_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=4,
        ).count()
        may_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=5,
        ).count()
        jun_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=6,
        ).count()
        jul_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=7,
        ).count()
        aug_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=8,
        ).count()
        sep_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=9,
        ).count()
        oct_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=10,
        ).count()
        nov_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=11,
        ).count()
        dec_completed_tasks_count = Task.objects.filter(
            status__name=StatusType.COMPLETED.value,
            updated_at__year=current_year,
            updated_at__month=12,
        ).count()

        context["task_counts"] = {
            "pending": pending_tasks_count,
            "in_progress": in_progress_tasks_count,
            "completed": completed_tasks_count,
            "cancelled": cancelled_tasks_count,
            "low_priority": low_priority_tasks_count,
            "medium_priority": medium_priority_tasks_count,
            "high_priority": high_priority_tasks_count,
            "critical_priority": critical_priority_tasks_count,
        }

        context["due_tasks_count_by_month"] = {
            "jan_due_tasks": jan_due_tasks_count,
            "feb_due_tasks": feb_due_tasks_count,
            "mar_due_tasks": mar_due_tasks_count,
            "apr_due_tasks": apr_due_tasks_count,
            "may_due_tasks": may_due_tasks_count,
            "jun_due_tasks": jun_due_tasks_count,
            "jul_due_tasks": jul_due_tasks_count,
            "aug_due_tasks": aug_due_tasks_count,
            "sep_due_tasks": sep_due_tasks_count,
            "oct_due_tasks": oct_due_tasks_count,
            "nov_due_tasks": nov_due_tasks_count,
            "dec_due_tasks": dec_due_tasks_count,
        }

        context["completed_tasks_count_by_month"] = {
            "jan_completed_tasks": jan_completed_tasks_count,
            "feb_completed_tasks": feb_completed_tasks_count,
            "mar_completed_tasks": mar_completed_tasks_count,
            "apr_completed_tasks": apr_completed_tasks_count,
            "may_completed_tasks": may_completed_tasks_count,
            "jun_completed_tasks": jun_completed_tasks_count,
            "jul_completed_tasks": jul_completed_tasks_count,
            "aug_completed_tasks": aug_completed_tasks_count,
            "sep_completed_tasks": sep_completed_tasks_count,
            "oct_completed_tasks": oct_completed_tasks_count,
            "nov_completed_tasks": nov_completed_tasks_count,
            "dec_completed_tasks": dec_completed_tasks_count,
        }

        return context


@method_decorator(limit_access, name="get")
class TaskView(LoginRequiredMixin, TemplateView):
    """Task page view."""

    template_name = "pages/tasks.html"

    def get_context_data(self, **kwargs: Any) -> Any:
        """Add context for the view."""

        context = super().get_context_data(**kwargs)

        pending_tasks_count = Task.objects.all().pending_tasks().count()
        in_progress_tasks_count = Task.objects.all().in_progress_tasks().count()
        completed_tasks_count = Task.objects.all().completed_tasks().count()
        cancelled_tasks_count = Task.objects.all().cancelled_tasks().count()

        task_list = Task.objects.all().order_by("-pk")

        context["task_counts"] = {
            "pending": pending_tasks_count,
            "in_progress": in_progress_tasks_count,
            "completed": completed_tasks_count,
            "cancelled": cancelled_tasks_count,
        }

        context["task_list"] = task_list

        return context


@method_decorator(limit_access, name="get")
class CreateTaskView(LoginRequiredMixin, FormView):
    """Create task view."""

    template_name = "pages/create_task.html"
    form_class = CreateTaskForm
    success_url = reverse_lazy("tasks")

    def form_valid(self, form: CreateTaskForm) -> HttpResponseRedirect:
        """Create new task."""

        user = self.request.user

        title = form.cleaned_data["title"]
        due_date = form.cleaned_data["due_date"]
        description = form.cleaned_data["description"]
        priority = form.cleaned_data["priority"]
        assigned_to = form.cleaned_data["assigned_to"]

        services.create_task(
            user=user,
            title=title,
            due_date=due_date,
            description=description,
            priority=priority,
            assigned_to=assigned_to,
        )
        return super().form_valid(form=form)


class TaskDetailsView(LoginRequiredMixin, TemplateView):
    """Task details view."""

    template_name = "pages/task_details.html"

    def get_context_data(self, **kwargs: Any) -> Any:
        """Add context for the view."""

        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get("pk")

        task = get_object_or_404(Task, pk=pk)

        context["task"] = task

        return context


@login_required
@require_http_methods(["POST", "GET"])
def task_update_view(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """Task update view."""

    data = get_object_or_404(Task, pk=pk)
    form = TaskUpdateForm(instance=data)

    if not request.user.is_superuser:
        form.fields["assigned_to"].widget.attrs["disabled"] = True

    if request.method == "POST":
        form = TaskUpdateForm(request.POST or None, instance=data)

        if not request.user.is_superuser:
            form.data = form.data.copy()
            form.data["assigned_to"] = data.assigned_to_id

        if form.is_valid():
            form.save()
            services.update_task(user=request.user, pk=pk)
            return HttpResponseRedirect(reverse("task_details", kwargs={"pk": pk}))

    context = {"form": form}
    return render(request, "pages/task_edit.html", context)


@login_required
@require_http_methods(["POST", "GET"])
@limit_access
def delete_task_view(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """Delete task view."""

    obj = get_object_or_404(Task, pk=pk)
    obj.delete()

    return HttpResponseRedirect(
        reverse(
            "tasks",
        )
    )


@method_decorator(limit_access, name="get")
class CalendarView(LoginRequiredMixin, TemplateView):
    """Calendarview."""

    template_name = "pages/calendar.html"

    def get_context_data(self, **kwargs: Any) -> Any:
        """Add context for the view."""

        context = super().get_context_data(**kwargs)

        return context


@login_required
@require_http_methods(["POST", "GET"])
@limit_access
def task_calendar_api(request: HttpRequest) -> Any:
    """Task api view."""

    tasks = Task.objects.all()
    events = []
    for task in tasks:
        events.append(
            {
                "id": task.id,
                "title": task.title,
                "start": task.due_date.strftime("%Y-%m-%d"),
                "description": task.description,
                "priority": task.priority.name,
                "priority_level_colour": task.priority.priority_level_colour,
                "status": task.status.name,
                "status_colour": task.status.status_colour,
            }
        )
    return JsonResponse(events, safe=False)


def delete_calendar_task(request: HttpRequest, task_id: int) -> Any:
    """Delete task api view."""

    if request.method == "DELETE":
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({"message": "Task deleted successfully"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


home_view = HomeView.as_view()
dashboard_view = DashboardView.as_view()
task_view = TaskView.as_view()
create_task_view = CreateTaskView.as_view()
task_details_view = TaskDetailsView.as_view()
calendar_view = CalendarView.as_view()
