from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import Event, RecurrencePattern, EventAttendee, Reminder


def create_example_event(organizer_username):
    organizer = User.objects.get(username=organizer_username)
    event = Event.objects.create(
        title='Team Sync',
        description='Weekly team sync meeting',
        start_time=datetime(2025, 1, 20, 10, 0),
        end_time=datetime(2025, 1, 20, 11, 0),
        organizer=organizer,
        status='scheduled',
        priority=2,
        location='Conference Room A'
    )
    return event


def create_recurring_example(organizer_username):
    organizer = User.objects.get(username=organizer_username)
    recurrence = RecurrencePattern.objects.create(
        frequency='weekly',
        interval=1,
        days_of_week='0,2,4',
        start_date=datetime(2025, 1, 20, 10, 0)
    )
    event = Event.objects.create(
        title='Weekly Standup',
        description='Recurring team standup',
        start_time=datetime(2025, 1, 20, 10, 0),
        end_time=datetime(2025, 1, 20, 10, 30),
        organizer=organizer,
        recurrence_pattern=recurrence,
        is_recurring=True,
        status='scheduled',
        priority=2,
        location='Zoom'
    )
    return event


def add_attendee_example(event, attendee_username):
    attendee = User.objects.get(username=attendee_username)
    EventAttendee.objects.create(event=event, attendee=attendee, rsvp_status='pending')


def create_reminder_example(event, user):
    Reminder.objects.create(
        event=event,
        user=user,
        reminder_type='email',
        minutes_before=30,
        scheduled_time=event.start_time - timedelta(minutes=30)
    )
