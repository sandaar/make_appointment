import datetime

from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils import timezone


class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronic_name = models.CharField(max_length=30)

    class Meta:
        unique_together = (('first_name', 'last_name', 'patronic_name'),)

    def __str__(self):
        return "{} {} {}".format(
            self.last_name, self.first_name, self.patronic_name)


class Appointment(models.Model):
    start_time = models.DateTimeField('Start date and time')
    end_time = models.DateTimeField('End date and time')
    doctor = models.ForeignKey(Doctor, null=True)
    first_name = models.CharField("Client's first name", max_length=30)
    last_name = models.CharField("Client's last name", max_length=30)
    patronic_name = models.CharField("Client's patronic name", max_length=30)

    def save(self, *args, **kwargs):
        self.clean()
        self.validate_unique()
        super(Appointment, self).save(*args, **kwargs)

    def clean(self):
        if self.start_time:
            self.end_time = self.start_time + datetime.timedelta(hours=1)
            if self.start_time <= timezone.now():
                raise ValidationError({'start_time': 'Past time'})
            if self.start_time.isoweekday() not in range(1, 6):
                raise ValidationError({'start_time': 'Not a business day'})
            if self.start_time.hour not in range(9, 18) or\
               self.end_time.hour not in range(9, 18):
                    raise ValidationError({'start_time': 'Not working hours'})

    def validate_unique(self, *args, **kwargs):
        super(Appointment, self).validate_unique(*args, **kwargs)

        qs = self.__class__._default_manager.filter(
            doctor=self.doctor,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )

        if not self._state.adding and self.pk is not None:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError({
                NON_FIELD_ERRORS: ['Appointment overlap', ],
            })

    def __str__(self):
        return "{} - {}: Appointment with Dr. {} {} {} ({} {} {})".format(
            self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            self.end_time.strftime("%H:%M:%S"),
            self.doctor.last_name,
            self.doctor.first_name,
            self.doctor.patronic_name,
            self.last_name,
            self.first_name,
            self.patronic_name)
