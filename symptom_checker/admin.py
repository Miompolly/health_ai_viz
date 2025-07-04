from django.contrib import admin
from .models import Disease, VitalSign

admin.site.register(Disease)
@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ('patient', 'disease', 'temperature', 'heart_rate', 'respiratory_rate', 'blood_pressure')
    list_filter = ('disease',)
    search_fields = ('patient__name', 'disease__name') 