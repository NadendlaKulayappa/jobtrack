
from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "job_title",
        "application_date",
        "status",
    )

    list_filter = ("status", "application_date")
    search_fields = ("company_name", "job_title")
 