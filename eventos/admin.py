from django.contrib import admin

# Register your models here.

from .models import eventos

class eventosAdmin(admin.ModelAdmin):
    readonly_fields=("fecha_registro","hora_registro", "id")

admin.site.register(eventos, eventosAdmin)

