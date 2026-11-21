# Smart Job Application Tracker

A Django-based web application that helps users manage job applications, track interview schedules, organize follow-ups, and prepare for interviews using AI.

## Features

- **Dashboard:** View job application statistics and application status.
- 
- **Application Management:** Add, update, delete, and track job applications.
- 
- **Search and Filtering:** Find applications by company, job title, or status.
- 
- **Application Status:** Track Applied, Assessment, Interview, Offered, and Rejected applications.
- 
- **Priority Management:** Organize applications by High, Medium, and Low priority.
- 
- **Interview Tracking:** Record interview dates, rounds, and preparation details.
- 
- **AI Interview Preparation:** Generate interview answers using the Groq API.
- 
- **Follow-up Management:** Record follow-up dates and notes.
- 
- **Email Reminders:** Support for interview and follow-up reminders.

## Technologies Used

- Python
- Django
- HTML
- CSS
- JavaScript
- PostgreSQL
- SQLite (local development)
- Groq API
- Git and GitHub

## Project Structure

```text
JobTrack/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── jobs/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── static/
├── manage.py
├── requirements.txt
├── build.sh
└── README.md
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/NadendlaKulayappa/jobtrack.git
```

2. Open the project folder:

```bash
cd jobtrack
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the virtual environment on Windows:

```powershell
.venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Configure your environment variables, including the Django secret key and any required API or database settings.

7. Apply database migrations:

```bash
python manage.py migrate
```

8. Run the development server:

```bash
python manage.py runserver
```

9. Open the application:

```text
http://127.0.0.1:8000/
```

## Live Deployment

The project is deployed using Render.

**Live Application:** https://jobtrack-1-ghto.onrender.com

## Future Enhancements

- User registration and secure login
- Improved interview preparation features
- Additional application analytics
- Enhanced reminder management

## Author

**Nadendla Kulayappa**

GitHub: https://github.com/NadendlaKulayappa

## License

This project is developed for educational and portfolio purposes.
