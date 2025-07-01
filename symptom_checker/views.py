# symptom_checker/views.py

from django.shortcuts import render
from .forms import UserSymptomForm
from .models import Disease, UserSymptom
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity

from django.contrib.auth import get_user_model
User = get_user_model()

from django.shortcuts import render
from .forms import UserSymptomForm
from .models import Disease, UserSymptom
from patients.models import Patient  # ✅ Added
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity

from django.shortcuts import render
from .forms import UserSymptomForm
from .models import Disease, UserSymptom
from patients.models import Patient  # ✅ Import Patient
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity


from django.shortcuts import render
from .forms import UserSymptomForm
from .models import Disease, UserSymptom
from patients.models import Patient
import os
import joblib
from sklearn.metrics.pairwise import cosine_similarity

def analyze_symptoms(request):
    form = UserSymptomForm()
    result = None
    matched_disease = None
    patient_name = None
    score_percentage = None
    submitted_symptoms = None

    if request.method == 'POST':
        form = UserSymptomForm(request.POST)
        if form.is_valid():
            user_symptom = form.save(commit=False)
            submitted_symptoms = user_symptom.symptoms

            try:
                # ✅ Check patient exists
                patient = Patient.objects.get(patient_id=user_symptom.patient_id.strip())
                patient_name = patient.name

                # Load model
                model_path = os.path.join(os.path.dirname(__file__), 'symptom_model.pkl')
                vectorizer, vectors, disease_names = joblib.load(model_path)

                # Predict disease
                input_vec = vectorizer.transform([user_symptom.symptoms])
                similarities = cosine_similarity(input_vec, vectors)
                best_idx = similarities.argmax()
                best_score = similarities[0, best_idx]
                score_percentage = round(best_score * 100, 2)

                if best_score > 0.2:
                    disease_name = disease_names[best_idx]
                    disease = Disease.objects.get(name=disease_name)
                    user_symptom.disease = disease
                    matched_disease = disease
                    result = disease_name
                else:
                    result = "No matching disease found."

                # ✅ Save only if patient exists
                user_symptom.save()

            except Patient.DoesNotExist:
                patient_name = None
                result = "Patient not found. No analysis done."

    return render(request, 'pages/symptom_checker.html', {
        'form': form,
        'result': result,
        'matched_disease': matched_disease,
        'patient_name': patient_name,
        'score_percentage': score_percentage,
        'submitted_symptoms': submitted_symptoms,
    })





from django.views.generic import ListView
from .models import Disease

class DiseaseListView(ListView):
    model = Disease
    template_name = 'pages/disease_list.html'
    context_object_name = 'diseases'