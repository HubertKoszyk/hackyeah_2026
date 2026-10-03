from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def get_parkings(request):
    return JsonResponse('hello all')


@require_GET
def get_parkings_by_id(request, id):
    JsonResponse('hello id')
    
