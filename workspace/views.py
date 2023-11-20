from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TemplateForm
import json


@csrf_exempt
def get_form(request):
    if request.method == 'POST':
        try:
            input_data = json.loads(request.body.decode('utf-8'))
            matching_template = TemplateForm.find_matching_template(input_data)
            if matching_template:
                return JsonResponse({'template_name': matching_template})
            else:
                typed_fields = TemplateForm.typeify_fields(input_data)
                return JsonResponse(typed_fields)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неправильный JSON формат'}, status=400)

    return JsonResponse({'error': 'Используйте метод POST'}, status=400)
