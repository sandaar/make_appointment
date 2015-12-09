from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.AppointmentCreateView.as_view(), name='index'),
    url(r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
]
