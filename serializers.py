from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, UserProfile, RecurrencePattern, Event, EventAttendee, Reminder


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'description']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'timezone', 'notification_enabled']


class RecurrencePatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurrencePattern
        fields = ['id', 'frequency', 'interval', 'days_of_week', 'start_date', 'end_date']


class EventAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendee
        fields = ['event', 'attendee', 'rsvp_status', 'response_date']


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['event', 'user', 'reminder_type', 'minutes_before', 'scheduled_time', 'is_sent']


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    attendees = EventAttendeeSerializer(source='attendee_records', many=True, read_only=True)
    recurrence_pattern = RecurrencePatternSerializer(read_only=True)
    reminders = ReminderSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'organizer', 'start_time', 'end_time',
            'duration_minutes', 'status', 'priority', 'location', 'is_virtual',
            'meeting_link', 'is_recurring', 'recurrence_pattern', 'attendees', 'reminders'
        ]
