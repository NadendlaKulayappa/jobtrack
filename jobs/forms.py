
from django import forms
from .models import JobApplication, InterviewPreparation


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication

        fields = [
            "company_name",
            "job_title",
            "application_date",
            "job_link",
            "status",
            "priority",
            "interview_date",
            "interview_time",
            "follow_up_date",
            "follow_up_time",
            "follow_up_note",
            "notes",
        ]

        widgets = {
            "application_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "interview_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "interview_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "follow_up_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "follow_up_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "job_link": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com/job"
                }
            ),
            "follow_up_note": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Example: Contact the recruiter for an update."
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add interview notes or other details..."
                }
            ),
        }


class InterviewPreparationForm(forms.ModelForm):

    class Meta:
        model = InterviewPreparation

        fields = [
            "application",
            "round_name",
            "interview_type",
            "scheduled_date",
            "preparation_status",
            "questions",
            "preparation_notes",
            "outcome",
        ]

        widgets = {
            "scheduled_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "questions": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Enter interview questions to practise..."
                }
            ),
            "preparation_notes": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Enter topics, study plans, and notes..."
                }
            ),
        }
