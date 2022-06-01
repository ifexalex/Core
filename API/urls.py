from django.urls import path

from .views import InBoundSms, OutBoundSms

urlpatterns = [
    path('inbound/sms/', InBoundSms.as_view(), name='inbound-sms'),
    path('outbound/sms/', OutBoundSms.as_view(), name='outbound-sms'),
] 


