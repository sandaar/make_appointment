import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Appointment, Doctor


class AppointmentMethodTests(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            first_name="test",
            last_name="test",
            patronic_name="test")

        now = timezone.now()
        # pick next Tuesday, 11am
        time = now + datetime.timedelta(days=-now.weekday()+1, weeks=1,
                                        hours=-now.hour+11)
        self.appointment = Appointment.objects.create(
            start_time=time, doctor=self.doctor,
            first_name="First", last_name="Last",
            patronic_name="Patronic")
        try:
            self.appointment.clean()
        except:
            self.fail("Encountered an unexpected exception.")

    def test_not_past_time(self):
        time = timezone.now() - datetime.timedelta(days=30)
        with self.assertRaisesRegexp(ValidationError, "Past time"):
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")

    def test_not_now(self):
        time = timezone.now()
        with self.assertRaisesRegexp(ValidationError, "Past time"):
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")

    def test_work_hours_nonwork_day(self):
        now = timezone.now()
        # pick next Saturday, work hour
        time = now + datetime.timedelta(days=-now.weekday()+5, weeks=1,
                                        hours=-now.hour+9)
        with self.assertRaisesRegexp(ValidationError, "Not a business day"):
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")

    def test_nonwork_hours_work_day(self):
        now = timezone.now()
        # pick next Monday, nonwork hour
        time = now + datetime.timedelta(days=-now.weekday(), weeks=1,
                                        hours=-now.hour)
        with self.assertRaisesRegexp(ValidationError, "Not working hours"):
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")

    def test_nonwork_hours_nonwork_day(self):
        now = timezone.now()
        # pick next Saturday, nonwork hour
        time = now + datetime.timedelta(days=-now.weekday()+5, weeks=1,
                                        hours=-now.hour)
        with self.assertRaisesRegexp(ValidationError, "Not a business day"):
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")

    def test_work_hours_work_day(self):
        now = timezone.now()
        # pick next Monday, work hour
        time = now + datetime.timedelta(days=-now.weekday(), weeks=1,
                                        hours=-now.hour+9)
        try:
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")
        except:
            self.fail("Encountered an unexpected exception.")

    def test_starts_during_ends_after(self):
        time = self.appointment.start_time + datetime.timedelta(minutes=30)
        with self.assertRaisesRegexp(ValidationError, "Appointment overlap"):
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")

    def test_starts_before_ends_during(self):
        time = self.appointment.start_time + datetime.timedelta(minutes=-30)
        with self.assertRaisesRegexp(ValidationError, "Appointment overlap"):
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")

    def test_starts_during_ends_during(self):
        time = self.appointment.start_time
        with self.assertRaisesRegexp(ValidationError, "Appointment overlap"):
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")

    def test_starts_before_ends_before(self):
        time = self.appointment.start_time + datetime.timedelta(hours=-1)
        try:
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")
        except:
            self.fail("Encountered an unexpected exception.")

    def test_starts_after_ends_after(self):
        time = self.appointment.start_time + datetime.timedelta(hours=1)
        try:
            Appointment.objects.create(start_time=time, doctor=self.doctor,
                                       first_name="First", last_name="Last",
                                       patronic_name="Patronic")
        except:
            self.fail("Encountered an unexpected exception.")
