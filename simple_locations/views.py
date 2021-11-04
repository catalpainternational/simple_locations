from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from mptt.exceptions import InvalidMove

from simple_locations.models import Area, AreaType, Point

from .forms import LocationForm


@cache_control(no_cache=True)
def simple_locations(request):
    """
    firefox likes to aggressively cache forms set cache control to false to override this
    """
    form = LocationForm()
    nodes = Area.tree.all()
    return render_to_response(
        "simple_locations/index.html",
        {
            "form": form,
            "nodes": nodes,
            "map_key": settings.MAP_KEY,
        },
        context_instance=RequestContext(request),
    )


def add_location(req, parent_id=None):
    nodes = Area.tree.all()

    if req.method == "POST":
        form = LocationForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            code = form.cleaned_data["code"]
            lat = form.cleaned_data["lat"]
            lon = form.cleaned_data["lon"]
            target = form.cleaned_data["target"]
            kind = form.cleaned_data["kind"]
            area = Area.objects.create(name=name, code=code, parent=target)
            if lat and lon:
                location = Point(latitude=lat, longitude=lon)
                location.save()
                area.location = location
            try:
                kind = get_object_or_404(AreaType, pk=int(kind))
                area.kind = kind
            except ValueError:
                pass
            area.save()
            form = LocationForm()

            return render_to_response(
                "simple_locations/location_edit.html",
                {"form": form, "nodes": nodes},
                context_instance=RequestContext(req),
            )
        else:
            form = LocationForm(req.POST)
            return render_to_response(
                "simple_locations/location_edit.html",
                {"form": form, "nodes": nodes},
                context_instance=RequestContext(req),
            )

    else:
        if parent_id:
            default_data = {}
            parent = get_object_or_404(Area, pk=parent_id)
            default_data["move_choice"] = True
            default_data["target"] = parent.pk
            default_data["position"] = "last-child"
            form = LocationForm(default_data)
            form._errors = ""
        else:
            form = LocationForm()

    return render_to_response(
        "simple_locations/location_edit.html",
        {"form": form, "nodes": nodes},
        context_instance=RequestContext(req),
    )


def edit_location(req, area_id):
    location = get_object_or_404(Area, pk=area_id)
    if req.method == "POST":
        form = LocationForm(req.POST)
        if form.is_valid():
            saved = True

            area = Area.objects.get(pk=area_id)
            area.name = form.cleaned_data["name"]
            area.code = form.cleaned_data["code"]
            lat = form.cleaned_data["lat"]
            lon = form.cleaned_data["lon"]
            kind = form.cleaned_data["kind"]

            try:
                kind = get_object_or_404(AreaType, pk=int(kind))
                area.kind = kind
            except ValueError:
                pass
            if lat and lon:
                point = Point(latitude=lat, longitude=lon)
                point.save()
                area.location = point
            try:
                area.save()
            except IntegrityError:
                form.errors["code"] = "This code already exists"
                saved = False

            if form.cleaned_data["move_choice"]:
                target = form.cleaned_data["target"]

                try:
                    area.parent = target
                    area.save()
                except InvalidMove:
                    form.errors["position"] = "This move is invalid"
                    saved = False

            if saved:
                form = LocationForm()
                return render_to_response(
                    "simple_locations/location_edit.html",
                    {"form": form, "nodes": Area.tree.all()},
                    context_instance=RequestContext(req),
                )
            else:
                return render_to_response(
                    "simple_locations/location_edit.html",
                    {"form": form, "item": location, "nodes": Area.tree.all()},
                    context_instance=RequestContext(req),
                )

        else:
            return render_to_response(
                "simple_locations/location_edit.html",
                {"form": form, "item": location},
                context_instance=RequestContext(req),
            )
    else:
        default_data = {}
        default_data["pk"] = location.pk
        default_data["name"] = location.name
        default_data["code"] = location.code
        default_data["move_choice"] = False
        if location.kind:
            default_data["kind"] = location.kind.pk
        if location.parent:
            default_data["target"] = location.parent
            default_data["position"] = "last-child"
        if location.location:
            default_data["lat"] = location.location.latitude
            default_data["lon"] = location.location.longitude
        form = LocationForm(default_data)
        return render_to_response(
            "simple_locations/location_edit.html",
            {"form": form, "nodes": Area.tree.all(), "item": location},
            context_instance=RequestContext(req),
        )


def delete_location(request, area_id):
    node = get_object_or_404(Area, pk=area_id)
    if request.method == "POST":
        node.delete()

    return HttpResponseRedirect("/simple_locations/render_tree")


@cache_control(no_cache=True)
def render_location(request):
    nodes = Area.tree.all()
    return render_to_response("simple_locations/treepanel.html", {"nodes": nodes})


def area_search(request):
    import json

    areadetails = []
    if request.GET.__contains__("query"):
        objects = Area.objects.filter(name__iregex=request.GET["query"])
    else:
        objects = Area.objects.all()
    for area in objects:
        areadetail = {}
        areadetail["value"] = area.pk
        areadetail["name"] = area.name
        areadetail["kind"] = area.kind.name

        if area.parent:
            areadetail["parentname"] = area.parent.name
            areadetail["parentkind"] = area.parent.kind.name
        areadetails.append(areadetail)
    return HttpResponse(json.dumps(areadetails))
