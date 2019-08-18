import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    if not value.name.endswith('.zip') or not value.name.endswith('.rar') or not value.name.endswith('.7z'):
       	raise ValidationError('Unsupported file extension.')