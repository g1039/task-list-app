"""Form classes for the tasktrack application."""

import datetime

from django import forms
from django_select2.forms import Select2Widget

from webapp.accounts.models import CustomUser
from webapp.tasktrack.models import Priority, Status, Task


class CreateTaskForm(forms.Form):
    """Create task form."""

    title = forms.CharField()
    due_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control datepicker",
                "placeholder": "Select a date",
            }
        ),
        required=False,
    )
    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )
    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
    )
    assigned_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_active=True), widget=Select2Widget
    )

    def clean_due_date(self) -> str:
        """Validate the provided due date."""

        due_date = self.cleaned_data.get("due_date")
        if due_date and due_date < datetime.date.today():
            raise forms.ValidationError(
                "Due date cannot be earlier than the creation date."
            )
        return due_date


class TaskUpdateForm(forms.ModelForm):
    """Task update form."""

    title = forms.CharField()
    due_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control datepicker",
                "placeholder": "Select a date",
            }
        ),
        required=False,
    )
    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )
    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
    )
    assigned_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_active=True), widget=Select2Widget
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "due_date",
            "description",
            "priority",
            "status",
            "assigned_to",
        ]


class CreateCalendarTaskForm(forms.ModelForm):
    """Create task form."""

    class Meta:
        model = Task
        fields = ["title", "due_date", "description", "priority", "assigned_to"]

        widgets = {
            "due_date": forms.TextInput(
                attrs={
                    "class": "form-control datepicker",
                    "placeholder": "Select a date",
                }
            ),
            "description": forms.Textarea(),
        }

    def clean_due_date(self) -> str:
        """Validate the provided due date."""

        due_date = self.cleaned_data.get("due_date")
        if due_date and due_date < datetime.date.today():
            raise forms.ValidationError(
                "Due date cannot be earlier than the creation date."
            )
        return due_date
