from django.views.generic.edit import CreateView

from .models import Appointment
from .forms import AppointmentForm


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = '/'
