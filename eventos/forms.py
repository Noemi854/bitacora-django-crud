from django.forms import ModelForm, DateField, DateInput
from .models import eventos
from django import forms
from datetime import date

class eventoForm (forms.ModelForm):
    fecha_evento = DateField(
        label="Fecha del Evento",
        required=True,
        widget=DateInput(format="%Y-%m-%d", attrs={"type": "date", "min": date.today().isoformat(), "class": "form-control"}),
        input_formats=["%Y-%m-%d"]
    )
    
    def clean_fecha_evento(self):
        fecha = self.cleaned_data.get('fecha_evento')
        if fecha and fecha < date.today():
            raise forms.ValidationError('No puedes seleccionar una fecha pasada')
        return fecha
    
    class Meta:
        model= eventos
        fields=['fecha_evento', 'local_afectado', 'tipo_evento', 'detalles_evento']
        labels={
            'fecha_evento': 'Fecha del Evento',
            'local_afectado': 'Local Afectado',
            'tipo_evento': 'Tipo de Evento',
            'detalles_evento': 'Detalles del Evento',
        }
        widgets={
            'local_afectado': forms.Select(attrs={'class': 'form-control'}),
            'tipo_evento': forms.Select(attrs={'class': 'form-control'}),
            'detalles_evento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }