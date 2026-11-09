
from django.db import models


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Assessment", "Assessment"),
        ("Interview", "Interview"),
        ("Offered", "Offered"),
        ("Rejected", "Rejected"),
    ]

    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    application_date = models.DateField()
    job_link = models.URLField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Applied",
    )

    # Job application priority
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium",
    )

    # Interview scheduling
    interview_date = models.DateField(null=True, blank=True)
    interview_time = models.TimeField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)

    # Follow-up scheduling
    follow_up_date = models.DateField(null=True, blank=True)
    follow_up_time = models.TimeField(null=True, blank=True)
    follow_up_note = models.TextField(blank=True)
    follow_up_reminder_sent = models.BooleanField(default=False)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"


class InterviewPreparation(models.Model):

    ROUND_CHOICES = [
        ("Phone Screening", "Phone Screening"),
        ("Technical Round", "Technical Round"),
        ("Coding Round", "Coding Round"),
        ("Managerial Round", "Managerial Round"),
        ("HR Round", "HR Round"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Not Started", "Not Started"),
        ("Preparing", "Preparing"),
        ("Completed", "Completed"),
    ]

    OUTCOME_CHOICES = [
        ("Pending", "Pending"),
        ("Passed", "Passed"),
        ("Failed", "Failed"),
        ("Rescheduled", "Rescheduled"),
    ]

    application = models.ForeignKey(
        "jobs.JobApplication",
        on_delete=models.CASCADE,
        related_name="preparation_records",
    )

    round_name = models.CharField(
        max_length=50,
        choices=ROUND_CHOICES,
    )

    interview_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: Online, In-person, Video call",
    )

    scheduled_date = models.DateField(
        null=True,
        blank=True,
    )

    preparation_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Not Started",
    )

    questions = models.TextField(
        blank=True,
        help_text="Questions you expect or want to practise",
    )

    ai_answer = models.TextField(
        blank=True,
        help_text="AI-generated interview answer",
    )

    preparation_notes = models.TextField(
        blank=True,
        help_text="Topics to study and preparation notes",
    )

    outcome = models.CharField(
        max_length=20,
        choices=OUTCOME_CHOICES,
        default="Pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application.company_name} - {self.round_name}"
