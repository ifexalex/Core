from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.exceptions import Throttled
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from API.serializers import InBoundSerializer, OutBoundSerializer
from .custom_throttling import CustomThrottle

# get_user_model() is a Django function that returns the User model
User = get_user_model()


class InBoundSms(APIView):

    """
    It takes a POST request with a JSON payload, validates the payload, and returns a JSON response

    :param from_: The sender number
    :param to: The destination number
    :param text: The sms text
    :return: The response is a JSON object:
    """

    serializer_class = InBoundSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        from_ = serializer.validated_data["from_"]
        to = serializer.validated_data["to"]
        text = serializer.validated_data["text"]

        # Creating a unique key for the cache.
        stop_id = from_ + to

        # Checking if the text starts with the word STOP and if it does, it sets a value for the key
        # `stop_id` in the cache.
        if text.startswith("STOP"):
            cache.set(stop_id, "TEST", timeout=240)
            cache.expire_at(stop_id, datetime.now() + timedelta(hours=4))

        return Response(
            {"status": True, "message": "inbound sms ok"},
            status=status.HTTP_200_OK,
        )


class OutBoundSms(APIView):

    """
    It takes a POST request with a JSON payload, validates the payload, and returns a JSON response

    :param from_: The sender number
    :param to: The destination number
    :param text: The sms text
    :return: The response is a JSON object:
    """

    serializer_class = OutBoundSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = "outbound"
    http_method_names = ["post"]
    throttle_classes = [CustomThrottle]

    def post(self, request, format=None):

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        from_ = serializer.validated_data["from_"]
        to = serializer.validated_data["to"]
        text = serializer.validated_data["text"]

        # Creating a unique key for the cache.
        stop_id = to + from_

        # Checking if the cache has a value for the key `stop_id` and if it does, it returns a
        # response with a status code of 403.
        if cache.get(stop_id):
            return Response(
                {
                    "status": False,
                    "message": "Stop message",
                    "error": "sms from {} to {} blocked by STOP request".format(
                        from_, to
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {"status": True, "message": "outbound sms ok"},
            status=status.HTTP_200_OK,
        )

    def throttled(self, request, wait):
        """
        If the request is throttled, then raise a Throttled exception with a detail message

        :param request: The request object
        :param wait: The number of seconds to wait before the request can be repeated
        """
        raise Throttled(
            detail={
                "message": "throttled",
                "error": "limit reached for from <{}>".format(request.data["from_"]),
            }
        )
