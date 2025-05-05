from django import forms
from .models import Event, UserProfile, Vendor
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['vendor', 'saved_by']
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
        
# forms.py
VENDOR_TYPES = (
        ('F', 'Food'),
        ('D', 'Drink'),
        ('C', 'Crafts'),
)
class CustomSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_vendor = forms.BooleanField(required=False, label="Are you a vendor?")

    # Vendor-specific fields
    vendor_type = forms.ChoiceField(choices=VENDOR_TYPES, required=False)
    primary_contact_name = forms.CharField(required=False)
    business_name = forms.CharField(required=False)
    business_email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2',
            'is_vendor', 'vendor_type', 'business_name', 'business_email'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Conditionally make vendor fields required
        if self.data.get('is_vendor') == 'on':  # or self.cleaned_data.get('is_vendor')
            self.fields['vendor_type'].required = True
            self.fields['primary_contact_name'].required = True
            self.fields['business_name'].required = True
            self.fields['business_email'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = UserProfile.objects.create(
                user=user,
                user_name=user.username,
            )
            if self.cleaned_data.get('is_vendor'):  # Ensure is_vendor is properly checked
                Vendor.objects.create(
                    user=user,
                    vendorType=self.cleaned_data['vendor_type'],
                    primary_contact_name=self.cleaned_data['primary_contact_name'],
                    business_name=self.cleaned_data['business_name'],
                    business_email=self.cleaned_data['business_email'],
                )
        return user
