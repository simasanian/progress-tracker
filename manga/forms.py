from django import forms
from .models import Project
from .models import Progress

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'total_pages', 'start_date', 'deadline', 'color']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['date', 'pages_done']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# Create your tests here.
