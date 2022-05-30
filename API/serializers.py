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
            raise serializers.ValidationError({"error":" to:{} is invalid".format(data.get("to"))})
        elif data.get("from_") not in  valid_from:
            raise serializers.ValidationError({"error":" from:{} is invalid".format(data.get("from_"))})
        elif not phone_query.exists():
            raise serializers.ValidationError({"error": "to:{} not found".format(data.get("to"))}) 
        elif data.get("from_") == data.get("to"):
            raise serializers.ValidationError({"error": "from {}: and to:{} parameter cannot be the same".format(data.get("from_"),data.get("to"))}) 
        return data


        

class OutBoundSerializer(InBoundSerializer):
    """
    Serializer for Sms parameters
    """
    
    def validate(self, data):

        # Checking if the number exists in the database.
        phone_query=  PhoneNumber.objects.filter(number=data.get("from_"))


       # Removing all non-numeric characters from the string.
        valid_to = re.sub("[^0-9]", "", data.get("to"))
        valid_from = re.sub("[^0-9]", "", data.get("from_"))

        if data.get("to") not in  valid_to:
            raise serializers.ValidationError({"error":"to:{} is invalid".format(data.get("to"))})
        elif data.get("from_") not in  valid_from:
            raise serializers.ValidationError({"error":"from:{} is invalid".format(data.get("from_"))})
        elif not phone_query.exists():
            raise serializers.ValidationError({"error": "from:{} not found".format(data.get("from_"))})
        elif data.get("from_") == data.get("to"):
            raise serializers.ValidationError({"error": "from {}: and to:{} parameter cannot be the same".format(data.get("from_"),data.get("to"))})
        return data