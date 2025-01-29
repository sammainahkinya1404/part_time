from django import forms
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'contact_info']

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['resume']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'salary', 'location', 'category']
