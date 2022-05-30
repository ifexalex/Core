from rest_framework import serializers
from django.core.validators import MinLengthValidator
from phone.models import PhoneNumber
import re


class InBoundSerializer(serializers.Serializer):
    """
    Serializer for Sms parameters
    """

    from_ = serializers.CharField(max_length=16, validators=[MinLengthValidator(6)])
    to = serializers.CharField(max_length=16, validators=[MinLengthValidator(6)])
    text = serializers.CharField(max_length=120, validators=[MinLengthValidator(1)])

    def validate(self, data):

        
        # Checking if the number exists in the database.
        phone_query=  PhoneNumber.objects.filter(number=data.get("to"))


       # Removing all non-numeric characters from the string.
        valid_to = re.sub("[^0-9]", "", data.get("to"))
        valid_from = re.sub("[^0-9]", "", data.get("from_"))

        if data.get("to") not in  valid_to:
            raise serializers.ValidationError({"message":" <{}> is invalid".format(valid_to)})
        elif data.get("from_") not in  valid_from:
            raise serializers.ValidationError({"message":" <{}> is invalid".format(valid_from)})
        elif not phone_query.exists():
            raise serializers.ValidationError({"status":False,"message": "<{}> not found".format(data.get("to"))}) 
        return data


        

class OutBoundSerializer(InBoundSerializer):
    
    def validate(self, data):

        # Checking if the number exists in the database.
        phone_query=  PhoneNumber.objects.filter(number=data.get("from_"))


       # Removing all non-numeric characters from the string.
        valid_to = re.sub("[^0-9]", "", data.get("to"))
        valid_from = re.sub("[^0-9]", "", data.get("from_"))

        if data.get("to") not in  valid_to:
            raise serializers.ValidationError({"status":False,"message":" invalid phone number"})
        elif data.get("from_") not in  valid_from:
            raise serializers.ValidationError({"status":False,"message":" invalid phone number"})
        elif not phone_query.exists():
            raise serializers.ValidationError({"status":False,"message": "<{}> not found".format(data.get("from_"))}) 
        return data