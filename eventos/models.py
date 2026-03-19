from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class eventos(models.Model):
    
    opciones_tipo_evento = [
        ('lluvia', 'Lluvia'),
        ('frio', 'Frio'),
        ('evento_deportivo', 'Evento Deportivo'),
        ('elecciones', 'Elecciones'),
        ('corte_de_suministro', 'Corte de Suministro'),
        ('cuarentena', 'Cuarentena'),
        ('desastre_natural', 'Desastre Natural'),
        ('trabajo_o_reparaciones', 'Trabajo o Reparaciones'),
        ('falla_de_equipos', 'Falla de Equipos'),
        ('dia_festivo', 'Día Festivo'),
        ('temas_productivos', 'Temas Productivos'),
        ('otros', 'Otros')
    ]
    
    opciones_local_afectado = [
        ('apoquindo', 'Apoquindo'),
        ('las_tranqueras', 'Las Tranqueras'),
        ('vitacura', 'Vitacura'),
        ('san_carlos_de_apoquindo', 'San Carlos de Apoquindo'),
        ('cristobal_colon', 'Cristobal Colon'),
        ('isabel_la_catolica', 'Isabel la Catolica'),
        ('luis_pasteur', 'Luis Pasteur'),
        ('la_dehesa', 'La Dehesa'),
        ('colina', 'Colina'),
        ]
        
        
    fecha_registro=models.DateField(auto_now_add=True)
    hora_registro=models.TimeField(auto_now_add=True)
    creador=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_evento=models.DateField()
    local_afectado=models.CharField(max_length=50, choices=opciones_local_afectado)
    tipo_evento=models.CharField(max_length=50, choices=opciones_tipo_evento)
    detalles_evento=models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_tipo_evento_display()} - {self.get_local_afectado_display()} - {self.fecha_evento}"
    
    