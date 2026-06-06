from django.contrib import admin
from .models import Role, UserProfile, RecurrencePattern, Event, EventAttendee, Reminder


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'timezone', 'notification_enabled', 'created_at']


@admin.register(RecurrencePattern)
class RecurrencePatternAdmin(admin.ModelAdmin):
    list_display = ['frequency', 'interval', 'start_date', 'end_date']
    list_filter = ['frequency']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'start_time', 'end_time', 'status', 'priority']
    list_filter = ['status', 'priority', 'is_virtual']
    search_fields = ['title', 'organizer__username']


@admin.register(EventAttendee)
class EventAttendeeAdmin(admin.ModelAdmin):
    list_display = ['event', 'attendee', 'rsvp_status', 'response_date']


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'reminder_type', 'minutes_before', 'scheduled_time', 'is_sent']
