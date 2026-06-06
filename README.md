# Scheduling System

A Django-based scheduling application prototype that includes core event models, admin setup, REST serializers, and usage examples.

This repository is designed as a standalone Django app to manage events, recurring schedules, attendees, and reminders. It is ideal for rapid prototyping, learning, or extending into a full scheduling product.

## Features

- Event creation with start/end times, status, and priority
- Recurring schedule patterns for repeated events
- Attendee management with RSVP tracking
- Reminder model for notification scheduling
- Django admin integration for easy administration
- DRF serializers for API-ready data

## Project Structure

- `models.py` — Core Django models for roles, events, recurring patterns, attendees, and reminders
- `admin.py` — Admin registration and admin list displays
- `serializers.py` — Django REST Framework serializers
- `examples.py` — Example usage functions for event creation and reminders
- `requirements.txt` — Python dependency list
- `settings_example.py` — Example Django settings snippet for SQLite

## Installation

```bash
pip install -r requirements.txt
```

## Setup

1. Add this app to your Django project's `INSTALLED_APPS`.
2. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser and run the server:

```bash
python manage.py createsuperuser
python manage.py runserver
```

## Usage

- Manage events, recurring patterns, attendees, and reminders through Django admin.
- Use `serializers.py` as a basis for REST API endpoints.
- Use `examples.py` to learn how to create events programmatically.

## Notes

- `settings_example.py` is a template; copy relevant configuration into your Django settings file.
- This repository is best used as an app inside a Django project or a learning prototype.

## License

Use this project under your preferred license, or add a `LICENSE` file to define terms.
