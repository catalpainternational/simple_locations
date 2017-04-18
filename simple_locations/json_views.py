from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.http import JsonResponse
import json

from .models import Area

def area(request, area_id):
    return JsonResponse(Area.geojson(area_id))

def children(request, area_id):
    return JsonResponse(Area.geojson(area_id, children=True))