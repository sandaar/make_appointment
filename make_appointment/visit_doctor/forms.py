from django.forms import ModelForm
from bootstrap3_datetime.widgets import DateTimePicker

from .models import Appointment


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        exclude = ['end_time']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = DateTimePicker(options={
            "format": "YYYY-MM-DD HH:mm", "pickSeconds": False})
