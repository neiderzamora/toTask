# rest_framawork
from rest_framework import serializers
from django.core.exceptions import ValidationError

# others
import re

""" Validator phone """

def validate_phone(value):
    pattern = r'^\d{10}$'
    if not re.match(pattern, value):
        raise serializers.ValidationError("El número de teléfono debe tener exactamente 10 dígitos.")
    return value