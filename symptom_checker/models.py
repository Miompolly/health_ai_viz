from django.db import models

class Disease(models.Model):
    name = models.CharField(max_length=255, unique=True)
    symptoms = models.TextField()
    test_results = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    medicine = models.TextField(blank=True, null=True)  # ✅ New field

    def __str__(self):
        return self.name
    

class UserSymptom(models.Model):
    patient_id = models.CharField(max_length=255)
    symptoms = models.TextField()
    disease = models.ForeignKey(Disease, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Symptoms for User {self.user_id} - {self.disease if self.disease else 'Unknown Disease'}"

    @property
    def recommendations(self):
        return self.disease.recommendation if self.disease else None

    @property
    def medicine(self):
        return self.disease.medicine if self.disease else None
    
from patients.models import Patient 

class VitalSign(models.Model):
    patient = models.ForeignKey(
        Patient,
        related_name='vital_signs', null=True, blank=True,
        on_delete=models.CASCADE
    )
    disease = models.ForeignKey(
        'Disease',
        related_name='vital_signs',
        on_delete=models.CASCADE
    )
    temperature = models.CharField(max_length=100, blank=True, null=True)
    heart_rate = models.CharField(max_length=100, blank=True, null=True)
    respiratory_rate = models.CharField(max_length=100, blank=True, null=True)
    blood_pressure = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vital signs for {self.patient} - {self.disease.name}"