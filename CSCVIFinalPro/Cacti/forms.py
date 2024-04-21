from django import forms
from .models import Profile
from .models import Cactus

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']  # Add other fields here


class CactusForm(forms.ModelForm):
    class Meta:
        model = Cactus
        fields = ['name', 'description', 'price']


class PaymentForm(forms.Form):
    name = forms.CharField(label='Name on Card', max_length=100)
    email = forms.EmailField(label='Email')
    card_number = forms.CharField(label='Card Number', max_length=16)
    expiration_date = forms.CharField(label='Expiration Date (MM/YY)', max_length=5)
    cvc = forms.CharField(label='CVC', max_length=4)
