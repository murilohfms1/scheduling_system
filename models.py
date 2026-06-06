from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta
import uuid


class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('organizer', 'Event Organizer'),
        ('attendee', 'Attendee'),
        ('viewer', 'Viewer Only'),
    ]

    name = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    notification_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"


class RecurrencePattern(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    interval = models.PositiveIntegerField(default=1)
    days_of_week = models.CharField(max_length=20, blank=True, help_text='Comma-separated weekday numbers 0=Mon')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_frequency_display()} every {self.interval}"

    def next_occurrences(self, count=5):
        occurrences = []
        current = self.start_date
        while len(occurrences) < count:
            if self.end_date and current > self.end_date:
                break
            occurrences.append(current)
            if self.frequency == 'daily':
                current += timedelta(days=self.interval)
            elif self.frequency == 'weekly':
                current += timedelta(weeks=self.interval)
            elif self.frequency == 'monthly':
                month = current.month + self.interval
                year = current.year + (month - 1) // 12
                month = (month - 1) % 12 + 1
                current = current.replace(year=year, month=month)
            elif self.frequency == 'yearly':
                current = current.replace(year=current.year + self.interval)
        return occurrences


class Event(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(User, through='EventAttendee', related_name='events')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    location = models.CharField(max_length=255, blank=True)
    is_virtual = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True, null=True)
    recurrence_pattern = models.ForeignKey('RecurrencePattern', null=True, blank=True, on_delete=models.SET_NULL, related_name='events')
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time')

    def save(self, *args, **kwargs):
        self.duration_minutes = int((self.end_time - self.start_time).total_seconds() / 60)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.start_time})"


class EventAttendee(models.Model):
    RSVP_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendee_records')
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    rsvp_status = models.CharField(max_length=20, choices=RSVP_CHOICES, default='pending')
    response_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('event', 'attendee')

    def __str__(self):
        return f"{self.attendee.username} - {self.event.title}"


class Reminder(models.Model):
    REMINDER_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_CHOICES)
    minutes_before = models.PositiveIntegerField(default=15)
    scheduled_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event.title} reminder ({self.reminder_type})"
