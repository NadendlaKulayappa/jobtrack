
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("applications/add/", views.application_create, name="application_create"),
    path("applications/<int:pk>/edit/", views.application_edit, name="application_edit"),
    path("applications/<int:pk>/delete/", views.application_delete, name="application_delete"),

    # Interview Preparation Tracker
    path(
        "interview-preparation/",
        views.interview_preparation_list,
        name="interview_preparation_list",
    ),
    path(
        "interview-preparation/add/",
        views.interview_preparation_create,
        name="interview_preparation_create",
    ),
    path(
        "interview-preparation/<int:pk>/edit/",
        views.interview_preparation_edit,
        name="interview_preparation_edit",
    ),
    path(
        "interview-preparation/<int:pk>/delete/",
        views.interview_preparation_delete,
        name="interview_preparation_delete",
    ),
    path(
    "interview-preparation/<int:pk>/generate-answer/",
    views.generate_interview_answer,
    name="generate_interview_answer",
),
]
