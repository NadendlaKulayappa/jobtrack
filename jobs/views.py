
import os
from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_POST

from groq import Groq

from .models import JobApplication, InterviewPreparation
from .forms import JobApplicationForm, InterviewPreparationForm


def home(request):
    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)

    all_applications = JobApplication.objects.all()

    # Search and status filtering
    applications = all_applications.order_by(
        "-application_date", "-id"
    )

    search_query = request.GET.get("q", "").strip()

    if search_query:
        applications = applications.filter(
            Q(company_name__icontains=search_query)
            | Q(job_title__icontains=search_query)
        )

    selected_status = request.GET.get("status", "")

    valid_statuses = [
        choice[0]
        for choice in JobApplication._meta.get_field("status").choices
    ]

    if selected_status in valid_statuses:
        applications = applications.filter(status=selected_status)
    else:
        selected_status = ""

    # Dashboard statistics
    total_applications = all_applications.count()
    interview_count = all_applications.filter(status="Interview").count()
    offer_count = all_applications.filter(status="Offered").count()
    rejected_count = all_applications.filter(status="Rejected").count()

    # Upcoming interviews
    upcoming_interviews = all_applications.filter(
        status="Interview",
        interview_date__gte=today,
    ).order_by("interview_date", "interview_time")

    # Upcoming and overdue follow-ups
    upcoming_followups = all_applications.filter(
        follow_up_date__gte=today,
    ).order_by("follow_up_date", "follow_up_time")

    overdue_followups = all_applications.filter(
        follow_up_date__lt=today,
    ).order_by("follow_up_date", "follow_up_time")

    # Application counts by status
    status_totals = {
        item["status"]: item["total"]
        for item in all_applications.values("status").annotate(
            total=Count("id")
        )
    }

    status_chart_labels = []
    status_chart_values = []

    for value, label in JobApplication._meta.get_field("status").choices:
        status_chart_labels.append(label)
        status_chart_values.append(status_totals.get(value, 0))

    # Monthly applications for the last six calendar months
    monthly_chart_labels = []
    monthly_chart_values = []

    current_month = today.replace(day=1)

    for offset in range(5, -1, -1):
        month_index = current_month.month - offset
        year = current_month.year

        while month_index <= 0:
            month_index += 12
            year -= 1

        month_start = date(year, month_index, 1)

        if month_index == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month_index + 1, 1)

        monthly_count = all_applications.filter(
            application_date__gte=month_start,
            application_date__lt=next_month,
        ).count()

        monthly_chart_labels.append(month_start.strftime("%b %Y"))
        monthly_chart_values.append(monthly_count)

    # Current status rates
    interview_rate = (
        round(interview_count / total_applications * 100, 1)
        if total_applications else 0
    )

    offer_rate = (
        round(offer_count / total_applications * 100, 1)
        if total_applications else 0
    )

    context = {
        "total_applications": total_applications,
        "interviews": interview_count,
        "offers": offer_count,
        "rejected": rejected_count,
        "search_query": search_query,
        "selected_status": selected_status,
        "status_choices": JobApplication._meta.get_field(
            "status"
        ).choices,
        "upcoming_interviews": upcoming_interviews,
        "upcoming_followups": upcoming_followups,
        "overdue_followups": overdue_followups,
        "today": today,
        "tomorrow": tomorrow,
        "status_chart_labels": status_chart_labels,
        "status_chart_values": status_chart_values,
        "monthly_chart_labels": monthly_chart_labels,
        "monthly_chart_values": monthly_chart_values,
        "interview_rate": interview_rate,
        "offer_rate": offer_rate,
    }

    # Five applications per page
    paginator = Paginator(applications, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context["page_obj"] = page_obj
    context["applications"] = page_obj.object_list

    return render(request, "jobs/home.html", context)


def application_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = JobApplicationForm()

    return render(
        request,
        "jobs/application_form.html",
        {"form": form, "page_title": "Add Job Application"},
    )


def application_edit(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)

    if request.method == "POST":
        form = JobApplicationForm(request.POST, instance=application)

        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = JobApplicationForm(instance=application)

    return render(
        request,
        "jobs/application_form.html",
        {"form": form, "page_title": "Edit Job Application"},
    )


def application_delete(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)

    if request.method == "POST":
        application.delete()
        return redirect("home")

    return render(
        request,
        "jobs/application_confirm_delete.html",
        {"application": application},
    )


def interview_preparation_list(request):
    preparations = InterviewPreparation.objects.select_related(
        "application"
    ).order_by("scheduled_date", "-created_at")

    return render(
        request,
        "jobs/interview_preparation_list.html",
        {"preparations": preparations},
    )


def interview_preparation_create(request):
    if request.method == "POST":
        form = InterviewPreparationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Interview preparation record added successfully.",
            )
            return redirect("interview_preparation_list")
    else:
        form = InterviewPreparationForm()

    return render(
        request,
        "jobs/interview_preparation_form.html",
        {
            "form": form,
            "page_title": "Add Interview Preparation",
        },
    )


def interview_preparation_edit(request, pk):
    preparation = get_object_or_404(InterviewPreparation, pk=pk)

    if request.method == "POST":
        form = InterviewPreparationForm(
            request.POST,
            instance=preparation,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Interview preparation record updated successfully.",
            )
            return redirect("interview_preparation_list")
    else:
        form = InterviewPreparationForm(instance=preparation)

    return render(
        request,
        "jobs/interview_preparation_form.html",
        {
            "form": form,
            "page_title": "Edit Interview Preparation",
        },
    )


def interview_preparation_delete(request, pk):
    preparation = get_object_or_404(InterviewPreparation, pk=pk)

    if request.method == "POST":
        preparation.delete()
        messages.success(
            request,
            "Interview preparation record deleted.",
        )
        return redirect("interview_preparation_list")

    return render(
        request,
        "jobs/interview_preparation_confirm_delete.html",
        {"preparation": preparation},
    )



@require_POST
def generate_interview_answer(request, pk):
    preparation = get_object_or_404(InterviewPreparation, pk=pk)
    question = preparation.questions.strip()

    if not question:
        messages.error(
            request,
            "Please add interview questions before generating an answer."
        )
        return redirect("interview_preparation_list")

    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        messages.error(
            request,
            "AI API key is missing. Restart the server after setting GROQ_API_KEY."
        )
        return redirect("interview_preparation_list")

    try:
        client = Groq(
            api_key=api_key,
            timeout=120.0,
            max_retries=1,
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an interview preparation coach for fresh graduates. "
                        "Answer in simple English. Explain concepts clearly, give "
                        "practical examples, and include code examples for programming "
                        "questions when useful. Format answers with headings and "
                        "bullet points for easy reading."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Company: {preparation.application.company_name}\n"
                        f"Job title: {preparation.application.job_title}\n"
                        f"Interview round: {preparation.round_name}\n\n"
                        f"Interview questions:\n{question}"
                    ),
                },
            ],
            temperature=0.4,
            max_tokens=1000,
        )

        answer = response.choices[0].message.content or ""

        if not answer.strip():
            messages.error(request, "The AI returned an empty answer. Please try again.")
            return redirect("interview_preparation_list")

        preparation.ai_answer = answer.strip()
        preparation.save(update_fields=["ai_answer", "updated_at"])

        messages.success(
            request,
            "AI answer generated and saved successfully!"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        messages.error(
            request,
            f"AI generation failed: {type(e).__name__}. "
            "Check the VS Code terminal for details."
        )

    return redirect("interview_preparation_list")
