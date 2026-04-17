from django.contrib import admin

from .models import CalendarSystem, MissingDatePolicy, SchedulePattern, Schedule
# Register your models here.

admin.site.register(CalendarSystem)
admin.site.register(MissingDatePolicy)
admin.site.register(SchedulePattern)
admin.site.register(Schedule)
