from django import forms
from .models import Piezas

class PiezasForm(forms.ModelForm):
    class Meta:
        model = Piezas
        fields = '__all__'
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }