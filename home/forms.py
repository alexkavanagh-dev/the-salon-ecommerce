from .models import FAQ, CustomerTestimonial
from django import forms


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ('question', 'answer',)


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = CustomerTestimonial
        fields = ('body',)
