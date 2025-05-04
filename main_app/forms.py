from django import forms
from .models import Item, Event

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['collection']
        widgets = {
            'purchase_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['vendor_id']
        widgets = {
            'start_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
            'end_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            )
            
        }