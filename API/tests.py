import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from phone.models import PhoneNumber
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.test import APITestCase, force_authenticate

from .serializers import OutBoundSerializer, OutBoundSerializer

User = get_user_model()


class InBoundSms(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.to = PhoneNumber.objects.create(
            account_id=self.user, number="4924195509198"
        )
        self.from_ = PhoneNumber.objects.create(
            account_id=self.user, number="4924195509196"
        )
        self.block_to = PhoneNumber.objects.create(
            account_id=self.user, number="441224459598"
        )
        self.block_from_ = PhoneNumber.objects.create(
            account_id=self.user, number="13605895047"
        )

    def test_inbound_sms_success(self):
        url = reverse("inbound-sms")
        data = {
            "from_": self.from_.number,
            "to": self.to.number,
            "text": "trial text",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], True)
        self.assertEqual(response.data["message"], "inbound sms ok")

    def test_inbound_sms_with_invalid_data(self):
        url = reverse("inbound-sms")
        data = {
            "from_": "dfghjveyvj",
            "to": "rtyujguyierf",
            "text": "trial text",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inbound_sms_not_a_vaild_to_phone_number(self):
        url = reverse("inbound-sms")
        data = {
            "from_": self.from_.number,
            "to": "123456789",
            "text": "trial text",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inbound_sms_with_invalid_authentication(self):
        url = reverse("inbound-sms")
        data = {
            "from_": self.from_.number,
            "to": self.to.number,
            "text": "trial text",
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inbound_sms_with_the_same_phone_number(self):
        url = reverse("inbound-sms")
        data = {
            "from_": self.from_.number,
            "to": self.from_.number,
            "text": "trial text",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inbound_sms_with_text_as_STOP_cache(self):
        url = reverse("inbound-sms")
        data = {
            "from_": self.block_from_.number,
            "to": self.block_to.number,
            "text": "STOP",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OutBoundSms(APITestCase):
    

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)

        self.to = PhoneNumber.objects.create(
            account_id=self.user, number="13605917249"
        )
        self.from_ = PhoneNumber.objects.create(
            account_id=self.user, number="441224459548"
        )
        self.block_from_ = PhoneNumber.objects.create(
            account_id=self.user, number="441224459598"
        )
        self.block_to = PhoneNumber.objects.create(
            account_id=self.user, number="13605895047"
        )
        self.limit_from_ = PhoneNumber.objects.create(
            account_id=self.user, number="441224459482"
        )
        self.limit_to = PhoneNumber.objects.create(
            account_id=self.user, number="441224980093"
        )





    def test_outbound_sms(self):
        url = reverse("outbound-sms")
        data = {
            "from_": self.from_.number,
            "to": self.to.number,
            "text": "trial text",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], True)
        self.assertEqual(response.data["message"], "outbound sms ok")


    def test_outbound_sms_with_invalid_data(self):
        url = reverse("outbound-sms")
        data = {
            "from_": "hggvuy",
            "to": "jguiuyihi",
            "text": "trial text",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_outbound_sms_not_a_valid_from_number(self):
        url = reverse("outbound-sms")
        data = {
            "from_": "244998048340",
            "to": self.from_.number,
            "text": "trial text",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_outbound_sms_with_invalid_authentication(self):
        url = reverse("outbound-sms")
        data = {
            "from_": self.from_.number,
            "to": self.to.number,
            "text": "trial text",
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_outbound_sms_with_the_same_phone_number(self):
        url = reverse("outbound-sms")
        data = {
            "from_": self.from_.number,
            "to": self.from_.number,
            "text": "trial text",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_outbound_sms_with_text_as_STOP_found_in_cache(self):
        url = reverse("outbound-sms")
        data = {
            "from_": self.block_from_.number,
            "to": self.block_to.number,
            "text": "trial text",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_outbound_sms_limit_reached(self):
        url = reverse("outbound-sms")
        data = {
            "from_": self.limit_from_.number,
            "to": self.limit_to.number,
            "text": "STOP",
        }
        for i in range(0, 50):
            response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

