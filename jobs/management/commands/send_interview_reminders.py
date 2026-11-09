
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.core.management.base import BaseCommand
from django.utils import timezone

from jobs.models import JobApplication


RECIPIENT_EMAIL = "abdhul0512@gmail.com"
REMINDER_MINUTES = 10


class Command(BaseCommand):
    help = "Send interview and follow-up reminders"

    def handle(self, *args, **options):
        now = timezone.localtime()
        window_end = now + timedelta(minutes=1)

        mailer = settings.MAILERS["default"]
        email_options = mailer["OPTIONS"]
        sender_email = email_options["username"]

        connection = get_connection()
        sent_count = 0

        try:
            # Interview reminders
            interviews = JobApplication.objects.filter(
                status="Interview",
                interview_date=now.date(),
                interview_time__isnull=False,
                reminder_sent=False,
            )

            for item in interviews:
                interview_datetime = timezone.make_aware(
                    datetime.combine(
                        item.interview_date,
                        item.interview_time,
                    ),
                    timezone.get_current_timezone(),
                )

                reminder_time = interview_datetime - timedelta(
                    minutes=REMINDER_MINUTES
                )

                if now <= reminder_time < window_end:
                    subject = f"Interview Reminder: {item.company_name}"
                    message = (
                        "Your interview is in approximately 10 minutes.\n\n"
                        f"Company: {item.company_name}\n"
                        f"Role: {item.job_title}\n"
                        f"Date: {item.interview_date}\n"
                        f"Time: {item.interview_time.strftime('%I:%M %p')}\n\n"
                        "Good luck!\nJobTrack"
                    )

                    try:
                        email = EmailMessage(
                            subject=subject,
                            body=message,
                            from_email=sender_email,
                            to=[RECIPIENT_EMAIL],
                            connection=connection,
                        )
                        email.send(fail_silently=False)

                        item.reminder_sent = True
                        item.save(update_fields=["reminder_sent"])
                        sent_count += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Interview reminder sent: {item.company_name}"
                            )
                        )
                    except Exception as error:
                        self.stderr.write(
                            f"Interview email failed for "
                            f"{item.company_name}: {error}"
                        )

            # Follow-up reminders
            followups = JobApplication.objects.filter(
                follow_up_date=now.date(),
                follow_up_time__isnull=False,
                follow_up_reminder_sent=False,
            )

            for item in followups:
                followup_datetime = timezone.make_aware(
                    datetime.combine(
                        item.follow_up_date,
                        item.follow_up_time,
                    ),
                    timezone.get_current_timezone(),
                )

                reminder_time = followup_datetime - timedelta(
                    minutes=REMINDER_MINUTES
                )

                if now <= reminder_time < window_end:
                    subject = f"Follow-up Reminder: {item.company_name}"
                    message = (
                        "Your job application follow-up is in approximately "
                        "10 minutes.\n\n"
                        f"Company: {item.company_name}\n"
                        f"Role: {item.job_title}\n"
                        f"Follow-up date: {item.follow_up_date}\n"
                        f"Follow-up time: "
                        f"{item.follow_up_time.strftime('%I:%M %p')}\n"
                        f"Note: {item.follow_up_note or 'No note added'}\n\n"
                        "JobTrack"
                    )

                    try:
                        email = EmailMessage(
                            subject=subject,
                            body=message,
                            from_email=sender_email,
                            to=[RECIPIENT_EMAIL],
                            connection=connection,
                        )
                        email.send(fail_silently=False)

                        item.follow_up_reminder_sent = True
                        item.save(
                            update_fields=["follow_up_reminder_sent"]
                        )
                        sent_count += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Follow-up reminder sent: {item.company_name}"
                            )
                        )
                    except Exception as error:
                        self.stderr.write(
                            f"Follow-up email failed for "
                            f"{item.company_name}: {error}"
                        )
        finally:
            connection.close()

        if sent_count == 0:
            self.stdout.write("No interview or follow-up reminders due now.")
