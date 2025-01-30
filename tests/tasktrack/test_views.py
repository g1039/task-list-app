import datetime

import pytest
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from tests.accounts.factories import CustomUserFactory
from tests.tasktrack.factories import PriorityFactory, StatusFactory, TaskFactory
from webapp.tasktrack.enums import PriorityLevel, StatusType
from webapp.tasktrack.models import Task
from webapp.tasktrack.views import DashboardView, HomeView


@pytest.mark.django_db
class TestHomeView:
    def test_home_view_redirects_for_anonymous_user(self, client: Client) -> None:
        response = client.get(reverse("home"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_home_view_renders_for_authenticated_user(self, client: Client) -> None:
        user = CustomUserFactory()
        client.force_login(user)

        response = client.get(reverse("home"))
        assert response.status_code == 200
        assert "pages/index.html" in [template.name for template in response.templates]

    def test_get_context_data(self, rf: RequestFactory) -> None:

        user = CustomUserFactory()

        priority = PriorityFactory()

        panding_status = StatusFactory(name=StatusType.PENDING)
        in_progress_status = StatusFactory(name=StatusType.IN_PROGRESS)
        completed_status = StatusFactory(name=StatusType.COMPLETED)
        cancelled_status = StatusFactory(name=StatusType.CANCELLED)

        TaskFactory.create_batch(
            3,
            due_date=timezone.now().date(),
            assigned_to=user,
            priority=priority,
            status=panding_status,
        )
        TaskFactory.create_batch(
            2,
            due_date=timezone.now().date(),
            assigned_to=user,
            priority=priority,
            status=in_progress_status,
        )
        TaskFactory.create_batch(
            5,
            due_date=timezone.now().date(),
            assigned_to=user,
            priority=priority,
            status=completed_status,
        )
        TaskFactory.create_batch(
            1,
            due_date=timezone.now().date(),
            assigned_to=user,
            priority=priority,
            status=cancelled_status,
        )

        request = rf.get(reverse("home"))
        request.user = user
        view = HomeView()
        view.request = request
        context = view.get_context_data()

        assert "task_counts" in context
        assert context["task_counts"]["pending"] == 3
        assert context["task_counts"]["in_progress"] == 2
        assert context["task_counts"]["completed"] == 5
        assert context["task_counts"]["cancelled"] == 1

        assert "task_list" in context
        assert context["task_list"].count() == 11

    def test_empty_task_list_context(self, rf: RequestFactory) -> None:

        user = CustomUserFactory()

        request = rf.get(reverse("home"))
        request.user = user
        view = HomeView()
        view.request = request
        context = view.get_context_data()

        assert context["task_counts"] == {
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "cancelled": 0,
        }
        assert list(context["task_list"]) == []


@pytest.mark.django_db
class TestDashboardView:
    def test_dashboard_view_redirects_for_anonymous_user(self, client: Client) -> None:

        response = client.get(reverse("dashboard"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_dashboard_view_renders_for_authenticated_user(
        self, client: Client
    ) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        response = client.get(reverse("dashboard"))
        assert response.status_code == 200
        assert "pages/dashboard.html" in [
            template.name for template in response.templates
        ]

    def test_get_context_data(self, rf: RequestFactory) -> None:

        user = CustomUserFactory()

        low_priority = PriorityFactory(name=PriorityLevel.LOW)
        medium_priority = PriorityFactory(name=PriorityLevel.MEDIUM)
        high_priority = PriorityFactory(name=PriorityLevel.HIGH)
        critical_priority = PriorityFactory(name=PriorityLevel.CRITICAL)

        panding_status = StatusFactory(name=StatusType.PENDING)
        in_progress_status = StatusFactory(name=StatusType.IN_PROGRESS)
        completed_status = StatusFactory(name=StatusType.COMPLETED)
        cancelled_status = StatusFactory(name=StatusType.CANCELLED)

        TaskFactory.create_batch(
            3,
            status=panding_status,
            priority=low_priority,
            due_date=timezone.now().date(),
            created_at=datetime.date(2025, 1, 1),
        )
        TaskFactory.create_batch(
            2,
            status=in_progress_status,
            priority=medium_priority,
            due_date=datetime.date(2025, 2, 1),
            created_at=datetime.date(2025, 1, 1),
        )
        TaskFactory.create_batch(
            5,
            status=completed_status,
            priority=high_priority,
            due_date=datetime.date(2025, 3, 15),
            updated_at=datetime.date(2025, 3, 10),
            created_at=datetime.date(2025, 1, 1),
        )
        TaskFactory.create_batch(
            1,
            status=cancelled_status,
            priority=critical_priority,
            due_date=datetime.date(2025, 4, 1),
            created_at=datetime.date(2025, 1, 1),
        )

        request = rf.get(reverse("dashboard"))
        request.user = user
        view = DashboardView()
        view.request = request
        context = view.get_context_data()

        assert "task_counts" in context
        assert context["task_counts"]["pending"] == 3
        assert context["task_counts"]["in_progress"] == 2
        assert context["task_counts"]["completed"] == 5
        assert context["task_counts"]["cancelled"] == 1

        assert context["task_counts"]["low_priority"] == 3
        assert context["task_counts"]["medium_priority"] == 2
        assert context["task_counts"]["high_priority"] == 5
        assert context["task_counts"]["critical_priority"] == 1

        assert "due_tasks_count_by_month" in context
        assert context["due_tasks_count_by_month"]["jan_due_tasks"] == 3
        assert context["due_tasks_count_by_month"]["feb_due_tasks"] == 2
        assert context["due_tasks_count_by_month"]["mar_due_tasks"] == 5
        assert context["due_tasks_count_by_month"]["apr_due_tasks"] == 1
        assert context["due_tasks_count_by_month"]["may_due_tasks"] == 0

        assert "completed_tasks_count_by_month" in context
        assert context["completed_tasks_count_by_month"]["jan_completed_tasks"] == 0
        assert context["completed_tasks_count_by_month"]["feb_completed_tasks"] == 0
        assert context["completed_tasks_count_by_month"]["mar_completed_tasks"] == 5
        assert context["completed_tasks_count_by_month"]["apr_completed_tasks"] == 0

    def test_empty_dashboard_context(self, rf: RequestFactory) -> None:

        user = CustomUserFactory()

        request = rf.get(reverse("dashboard"))
        request.user = user
        view = DashboardView()
        view.request = request
        context = view.get_context_data()

        assert context["task_counts"] == {
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "cancelled": 0,
            "low_priority": 0,
            "medium_priority": 0,
            "high_priority": 0,
            "critical_priority": 0,
        }

        assert context["due_tasks_count_by_month"] == {
            "jan_due_tasks": 0,
            "feb_due_tasks": 0,
            "mar_due_tasks": 0,
            "apr_due_tasks": 0,
            "may_due_tasks": 0,
            "jun_due_tasks": 0,
            "jul_due_tasks": 0,
            "aug_due_tasks": 0,
            "sep_due_tasks": 0,
            "oct_due_tasks": 0,
            "nov_due_tasks": 0,
            "dec_due_tasks": 0,
        }

        assert context["completed_tasks_count_by_month"] == {
            "jan_completed_tasks": 0,
            "feb_completed_tasks": 0,
            "mar_completed_tasks": 0,
            "apr_completed_tasks": 0,
            "may_completed_tasks": 0,
            "jun_completed_tasks": 0,
            "jul_completed_tasks": 0,
            "aug_completed_tasks": 0,
            "sep_completed_tasks": 0,
            "oct_completed_tasks": 0,
            "nov_completed_tasks": 0,
            "dec_completed_tasks": 0,
        }


@pytest.mark.django_db
class TestTaskView:
    def test_task_view_redirects_for_anonymous_user(self, client: Client) -> None:

        response = client.get(reverse("tasks"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_task_view_renders_for_authenticated_user(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        response = client.get(reverse("tasks"))
        assert response.status_code == 200
        assert "pages/tasks.html" in [template.name for template in response.templates]

    def test_task_view_context_data(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        low_priority = PriorityFactory(name=PriorityLevel.LOW)
        medium_priority = PriorityFactory(name=PriorityLevel.MEDIUM)

        status = StatusFactory(name=StatusType.PENDING)
        TaskFactory(
            due_date=timezone.now().date(), priority=low_priority, status=status
        )
        TaskFactory(
            due_date=timezone.now().date(), priority=medium_priority, status=status
        )

        response = client.get(reverse("tasks"))

        assert response.context["task_counts"]["pending"] == 2
        assert response.context["task_counts"]["in_progress"] == 0
        assert response.context["task_counts"]["completed"] == 0
        assert response.context["task_counts"]["cancelled"] == 0
        assert len(response.context["task_list"]) == 2


@pytest.mark.django_db
class TestCreateTaskView:
    def test_create_task_view_redirects_for_anonymous_user(
        self, client: Client
    ) -> None:

        response = client.get(reverse("create_task"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_create_task_view_renders_for_authenticated_user(
        self, client: Client
    ) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        response = client.get(reverse("create_task"))
        assert response.status_code == 200
        assert "pages/create_task.html" in [
            template.name for template in response.templates
        ]

    def test_create_task_form_submission_valid(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        priority = PriorityFactory()
        status = StatusFactory(name=StatusType.PENDING)
        assigned_to = CustomUserFactory()

        form_data = {
            "title": "Test Task",
            "due_date": datetime.date(2025, 2, 1),
            "description": "Test task description",
            "priority": priority.id,
            "assigned_to": assigned_to.id,
            "status": status.id,
        }

        response = client.post(reverse("create_task"), data=form_data)

        assert Task.objects.count() == 1
        task = Task.objects.first()
        assert task.title == "Test Task"
        assert task.due_date == datetime.date(2025, 2, 1)
        assert task.description == "Test task description"
        assert task.priority == priority
        assert task.status == status
        assert task.assigned_to == assigned_to
        assert task.created_by == user

        assert response.status_code == 302
        assert response.url == reverse("tasks")

    def test_create_task_form_submission_invalid(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        priority = PriorityFactory()
        status = StatusFactory(name=StatusType.PENDING)
        assigned_to = CustomUserFactory()

        form_data = {
            "title": "",
            "due_date": datetime.date(2025, 2, 1),
            "description": "Test task description",
            "priority": priority.id,
            "assigned_to": assigned_to.id,
            "status": status.id,
        }

        response = client.post(reverse("create_task"), data=form_data)

        assert response.status_code == 200
        assert "This field is required" in response.content.decode()

        assert Task.objects.count() == 0


@pytest.mark.django_db
class TestTaskDetailsView:
    def test_task_details_view_redirects_for_anonymous_user(
        self, client: Client
    ) -> None:

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1), created_at=timezone.now().date()
        )
        url = reverse("task_details", kwargs={"pk": task.pk})

        response = client.get(url)
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_task_details_view_renders_for_authenticated_user(
        self, client: Client
    ) -> None:

        user = CustomUserFactory()
        client.force_login(user)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            assigned_to=user,
            created_at=timezone.now().date(),
        )
        url = reverse("task_details", kwargs={"pk": task.pk})

        response = client.get(url)
        assert response.status_code == 200
        assert task.title in response.content.decode()


@pytest.mark.django_db
class TestTaskUpdateView:
    def test_task_update_view_redirects_for_anonymous_user(
        self, client: Client
    ) -> None:

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1), created_at=timezone.now().date()
        )
        url = reverse("task_update", kwargs={"pk": task.pk})

        response = client.get(url)
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_task_update_view_renders_for_authenticated_user(
        self, client: Client
    ) -> None:

        user = CustomUserFactory()
        client.force_login(user)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            assigned_to=user,
            created_at=timezone.now().date(),
        )
        url = reverse("task_update", kwargs={"pk": task.pk})

        response = client.get(url)
        assert response.status_code == 200
        assert task.title in response.content.decode()

    def test_superuser_can_edit_assigned_to_field(self, client: Client) -> None:

        superuser = CustomUserFactory(is_superuser=True)
        client.force_login(superuser)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            assigned_to=superuser,
            created_at=timezone.now().date(),
        )
        url = reverse("task_update", kwargs={"pk": task.pk})

        response = client.get(url)
        form = response.context["form"]
        assert not form.fields["assigned_to"].widget.attrs.get("disabled")

    def test_non_superuser_cannot_edit_assigned_to_field(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=False)
        client.force_login(user)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            assigned_to=user,
            created_at=timezone.now().date(),
        )
        url = reverse("task_update", kwargs={"pk": task.pk})

        response = client.get(url)
        form = response.context["form"]
        assert form.fields["assigned_to"].widget.attrs.get("disabled") is not None

    def test_task_update_view_form_submission_valid(self, client: Client) -> None:

        user = CustomUserFactory()
        client.force_login(user)

        task = TaskFactory(
            title="Old Task Title",
            due_date=datetime.date(2025, 12, 1),
            assigned_to=user,
            created_at=timezone.now().date(),
        )
        new_title = "Updated Task Title"
        url = reverse("task_update", kwargs={"pk": task.pk})

        form_data = {
            "title": new_title,
            "due_date": task.due_date,
            "description": task.description,
            "priority": task.priority.id,
            "status": task.status.id,
            "assigned_to": task.assigned_to.id,
        }

        response = client.post(url, data=form_data)

        task.refresh_from_db()
        assert task.title == new_title

        assert response.status_code == 302
        assert response.url == reverse("task_details", kwargs={"pk": task.pk})

    def test_task_update_view_form_submission_invalid(self, client: Client) -> None:

        user = CustomUserFactory()
        client.force_login(user)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            assigned_to=user,
            created_at=timezone.now().date(),
        )
        url = reverse("task_update", kwargs={"pk": task.pk})

        form_data = {
            "title": "",
            "due_date": task.due_date,
            "description": task.description,
            "priority": task.priority.id,
            "status": task.status,
            "assigned_to": task.assigned_to.id,
        }

        response = client.post(url, data=form_data)

        assert response.status_code == 200
        assert "This field is required" in response.content.decode()


@pytest.mark.django_db
class TestDeleteTaskView:
    def test_delete_task_view_redirects_for_anonymous_user(
        self, client: Client
    ) -> None:

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1), created_at=timezone.now().date()
        )
        url = reverse("delete_task", kwargs={"pk": task.pk})

        response = client.get(url)
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_authenticated_user_can_delete_task(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            assigned_to=user,
            created_at=timezone.now().date(),
        )
        url = reverse("delete_task", kwargs={"pk": task.pk})

        response = client.post(url)

        assert Task.objects.count() == 0

        assert response.status_code == 302
        assert response.url == reverse("tasks")

    def test_authenticated_user_cannot_delete_non_existent_task(
        self, client: Client
    ) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        non_existent_task_id = 1111
        url = reverse("delete_task", kwargs={"pk": non_existent_task_id})

        response = client.post(url)

        assert response.status_code == 404

    def test_authenticated_user_redirect_after_deleting_task(
        self, client: Client
    ) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            assigned_to=user,
            created_at=timezone.now().date(),
        )
        url = reverse("delete_task", kwargs={"pk": task.pk})

        response = client.post(url)

        assert Task.objects.count() == 0

        assert response.status_code == 302
        assert response.url == reverse("tasks")


@pytest.mark.django_db
class TestTaskCalendarAPI:
    def test_task_calendar_api_redirects_for_anonymous_user(
        self, client: Client
    ) -> None:

        url = reverse("task_calendar_api")
        response = client.get(url)

        assert response.status_code == 302
        assert "/login/" in response.url

    def test_authenticated_user_can_fetch_tasks(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            created_at=timezone.now().date(),
            created_by=user,
            updated_by=user,
        )

        url = reverse("task_calendar_api")
        response = client.get(url)

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

        task_data = data[0]
        assert task_data["id"] == task.id
        assert task_data["title"] == task.title
        assert task_data["start"] == task.due_date.strftime("%Y-%m-%d")
        assert task_data["description"] == task.description
        assert task_data["priority"] == task.priority.name
        assert task_data["priority_level_colour"] == task.priority.priority_level_colour
        assert task_data["status"] == task.status.name
        assert task_data["status_colour"] == task.status.status_colour

    def test_authenticated_user_sees_empty_list_when_no_tasks_exist(
        self, client: Client
    ) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        url = reverse("task_calendar_api")
        response = client.get(url)

        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.django_db
class TestDeleteCalendarTaskAPI:
    def test_authenticated_user_can_delete_task(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            assigned_to=user,
            created_at=timezone.now().date(),
        )
        url = reverse("delete_calendar_task", kwargs={"task_id": task.id})

        response = client.delete(url)

        assert response.status_code == 200
        assert response.json() == {"message": "Task deleted successfully"}
        assert not Task.objects.filter(id=task.id).exists()

    def test_invalid_request_method_returns_error(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        task = TaskFactory(
            due_date=datetime.date(2025, 12, 1),
            assigned_to=user,
            created_at=timezone.now().date(),
        )
        url = reverse("delete_calendar_task", kwargs={"task_id": task.id})

        response = client.get(url)

        assert response.status_code == 400
        assert response.json() == {"error": "Invalid request"}
        assert Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
class TestCreateTaskAPI:
    def test_create_task_requires_authentication(self, client: Client) -> None:

        url = reverse("create_task")
        response = client.post(url, data={})

        assert response.status_code == 302
        assert "/login/" in response.url

    def test_authenticated_user_can_create_task(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        url = reverse("create_task")

        priority = PriorityFactory()
        status = StatusFactory(name=StatusType.PENDING)
        assigned_to = CustomUserFactory()

        form_data = {
            "title": "New Task",
            "due_date": datetime.date(2025, 2, 1).isoformat(),
            "description": "Test task description",
            "priority": priority.id,
            "assigned_to": assigned_to.id,
            "status": status.id,
        }

        response = client.post(
            url,
            data=form_data,
        )

        assert response.status_code == 302
        assert Task.objects.count() == 1

        task = Task.objects.first()
        assert task.title == "New Task"
        assert task.created_by == user
        assert task.updated_by == user
        assert task.status.name == status.name

    def test_create_task_with_invalid_data(self, client: Client) -> None:

        user = CustomUserFactory(is_superuser=True)
        client.force_login(user)

        url = reverse("create_task")

        priority = PriorityFactory()
        status = StatusFactory(name=StatusType.PENDING)
        assigned_to = CustomUserFactory()

        form_data = {
            "title": "",
            "due_date": datetime.date(2020, 2, 1).isoformat(),
            "description": "Test task description",
            "priority": priority.id,
            "assigned_to": assigned_to.id,
            "status": status.id,
        }
        response = client.post(url, data=form_data)

        assert response.status_code == 200
