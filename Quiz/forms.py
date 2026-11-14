from django import forms
from .models import Participant


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'student_class', 'age', 'gender', 'institution', 'phone']
        labels = {
            'name': 'Name',
            'student_class': 'Class',
            'age': 'Age',
            'gender': 'Gender',
            'institution': 'Institution',
            'phone': 'Phone',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_class': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
