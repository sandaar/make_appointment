from django.contrib import admin

from .models import Doctor, Appointment


class AppointmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                        {'fields': ['doctor']}),
        ("Client's Information",      {'fields': [
                                                  'last_name',
                                                  'first_name',
                                                  'patronic_name'],
                                       'classes': ['collapse']}),
        ('Time and Date Information', {'fields': ['start_time',
                                                  'end_time'],
                                       'classes': ['collapse']}),
    ]
    list_display = ('doctor', 'start_time', 'end_time',
                    'last_name', 'first_name', 'patronic_name')
    list_filter = ['start_time']
    search_fields = ['last_name', 'first_name', 'patronic_name']


class AppointmentInline(admin.TabularInline):
    model = Appointment


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronic_name')
    inlines = [AppointmentInline]

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
