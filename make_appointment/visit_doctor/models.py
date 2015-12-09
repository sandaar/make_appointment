from django.db import models


class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronic_name = models.CharField(max_length=30)

    def __str__(self):
        return "{} {} {}".format(
                    self.last_name, self.first_name, self.patronic_name)


class Appointment(models.Model):
    start_time = models.DateTimeField('Start date and time')
    end_time = models.DateTimeField('End date and time')
    doctor = models.ForeignKey(Doctor)
    first_name = models.CharField("Client's first name", max_length=30)
    last_name = models.CharField("Client's last name", max_length=30)
    patronic_name = models.CharField("Client's patronic name", max_length=30)

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
