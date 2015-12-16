import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Appointment, Doctor
from .forms import AppointmentForm


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


class AppointmentFormTests(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            first_name="test",
            last_name="test",
            patronic_name="test")

    def test_init(self):
        AppointmentForm()

    def test_valid_data(self):
        now = timezone.now()
        # pick next Tuesday, 11am
        time = now + datetime.timedelta(days=-now.weekday()+1, weeks=1,
                                        hours=-now.hour+11)
        form = AppointmentForm({
            'start_time': time,
            'first_name': 'First',
            'last_name': 'Last',
            'patronic_name': 'Patronic',
            'doctor': self.doctor.id
            })
        self.assertTrue(form.is_valid())
        appointment = form.save()
        self.assertEqual(appointment.start_time, time)
        self.assertEqual(appointment.first_name, 'First')
        self.assertEqual(appointment.last_name, 'Last')
        self.assertEqual(appointment.patronic_name, 'Patronic')
        self.assertEqual(appointment.doctor, self.doctor)

    def test_blank_data(self):
        form = AppointmentForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'start_time': ['This field is required.'],
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'patronic_name': ['This field is required.'],
            'doctor': ['This field is required.']
            })


class AppointmentCreateViewTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_uses_right_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'visit_doctor/appointment_form.html')
