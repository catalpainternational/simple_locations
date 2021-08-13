from django import forms
from django.forms.utils import ErrorList
from mptt.forms import TreeNodeChoiceField

from simple_locations.models import Area, AreaType


class LocationForm(forms.Form):
    name = forms.CharField(max_length=100)
    code = forms.CharField(max_length=50, required=False)
    pk = forms.CharField(widget=forms.HiddenInput(), required=False)
    target = TreeNodeChoiceField(queryset=Area.tree.all(), level_indicator="++", required=False)
    lat = forms.DecimalField(required=False)
    lon = forms.DecimalField(required=False)
    kind = forms.ModelChoiceField(
        required=False,
        empty_label="-----",
        queryset=AreaType.objects.all(),
        to_field_name="name",
    )
    move_choice = forms.BooleanField(required=False)
    position = forms.ChoiceField(
        choices=(("last-child", "inside"), ("left", "before"), ("right", "after")),
        required=False,
    )

    def clean(self):
        """make sure that both lat and lon are provided. if lat is given then lon is also required and vice versa."""
        lat = self.cleaned_data["lat"]
        lon = self.cleaned_data["lon"]
        if not lat and lon:
            msg = "Please provide the latitude"
            self._errors["lat"] = ErrorList([msg])
            return ""
        elif lat and not lon:
            msg = "Please provide the longitude"
            self._errors["lon"] = ErrorList([msg])
            return ""
        if lat and lon:
            if not -90 <= lat <= 90:
                msg = "Invalid latitude must be between 90 and -90"
                self._errors["lat"] = ErrorList([msg])
                return ""
            if not -180 <= lon <= 180:
                msg = "Invalid latitude must be between 180 and -180"
                self._errors["lon"] = ErrorList([msg])
                return ""

        return self.cleaned_data
