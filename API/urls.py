from django.urls import path
from rest_framework import permissions
from .views import InBoundSms, OutBoundSms
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Creating a swagger schema view for the API.
schema_view = get_schema_view(
    openapi.Info(
        title="SMS API",
        default_version="v1",
        description="Microservice for sending SMS messages.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('inbound/sms/', InBoundSms.as_view(), name='inbound-sms'),
    path('outbound/sms/', OutBoundSms.as_view(), name='outbound-sms'),
    path(
        "apiDocs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] 


