from django import forms
from .models import Record, Item

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            "related_item",
            "quantity",
            "action_start_time",
            "action_end_time",
            "action_date",
            "happened",
            "record_notes",
        ]
        widgets = {
            "action_date": forms.DateInput(attrs={"type": "date"}),
            "action_start_time": forms.TimeInput(attrs={"type": "time"}),
            "action_end_time": forms.TimeInput(attrs={"type": "time"}),
        }
