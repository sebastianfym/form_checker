import re

from django.db import models
from tinydb import TinyDB, Query

db = TinyDB('db.json')


class TemplateForm(models.Model):
    name = models.CharField(max_length=255)
    fields = models.JSONField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # После сохранения в Django, обновляем данные в TinyDB
        db.insert({'name': self.name, 'fields': self.fields})

    @staticmethod
    def find_matching_template(input_fields):
        for template in db.all():
            template_fields = template['fields']
            if all(field in input_fields.items() for field in template_fields):
                return template['name']
        return None

    @staticmethod
    def typeify_fields(input_fields):
        type_map = {
            'date': 'date',
            'phone': 'phone',
            'email': 'email',
            'text': 'text'
        }
        typed_fields = {}
        for field, value in input_fields.items():
            typed_fields[field] = type_map.get(TemplateForm.validate_field(field, value), 'text')
        return typed_fields

    @staticmethod
    def validate_field(field, value):
        if 'phone' in field:
            phone_pattern = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'
            if re.match(phone_pattern, value):
                return 'phone'
            else:
                return 'text'

        elif 'date' in field:
            date_pattern = r'^(\d{4}-\d{2}-\d{2})|(\d{2}.\d{2}.\d{4})$'
            if re.match(date_pattern, value):
                return 'date'
            else:
                return 'text'

        elif 'email' in field:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_pattern, value):
                return 'email'
            else:
                return 'text'

        return 'text'

