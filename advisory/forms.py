from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FarmInput, Contact, PesticideShop

class FarmInputForm(forms.ModelForm):
    class Meta:
        model = FarmInput
        fields = '__all__'
        exclude = ['created_at']
        
        widgets = {
            'state': forms.Select(attrs={'class': 'form-select'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'crop': forms.Select(attrs={'class': 'form-select'}),
            'manual_crop': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter crop name', 'id': 'id_manual_crop_input'}),
            'season': forms.Select(attrs={'class': 'form-select'}),
            'sowing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'field_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'irrigation': forms.Select(attrs={'class': 'form-select'}),
            'soil_type': forms.Select(attrs={'class': 'form-select'}),
            'soil_health_card': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'seed_variety': forms.Select(attrs={'class': 'form-select'}),
            'pest_presence': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'state': 'State',
            'district': 'District',
            'crop': 'Crop Type',
            'manual_crop': 'Manual Crop Entry',
            'season': 'Growing Season',
            'sowing_date': 'Sowing Date',
            'field_area': 'Field Area (hectares)',
            'irrigation': 'Irrigation Type',
            'soil_type': 'Soil Type',
            'soil_health_card': 'Soil Health Card Available?',
            'seed_variety': 'Seed Variety',
            'pest_presence': 'Pest/Disease Present?',
        }

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject of your message'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us how we can help you...'}),
        }

class PesticideShopForm(forms.ModelForm):
    class Meta:
        model = PesticideShop
        fields = ['shop_name', 'owner_name', 'phone', 'email', 'state', 'district', 'address', 'pincode', 'pesticides_available']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop Name', 'id': 'id_shop_name'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner Name', 'id': 'id_owner_name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number', 'id': 'id_phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'shop@example.com (optional)', 'id': 'id_email'}),
            'state': forms.Select(attrs={'class': 'form-select', 'id': 'id_state'}),
            'district': forms.Select(attrs={'class': 'form-select', 'id': 'id_district'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Complete shop address', 'id': 'id_address'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '6-digit pincode', 'id': 'id_pincode'}),
            'pesticides_available': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'List pesticides available (e.g., Neem Oil, Chlorpyrifos, Imidacloprid)', 'id': 'id_pesticides_available'}),
        }
