import os
import django
import json

# 1. Set Django settings environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_ai_viz.settings')

# 2. Setup Django
django.setup()

# 3. Import model (after setup)
from symptom_checker.models import Disease

# 4. Load JSON data
with open('diseases.json', 'r') as f:
    data = json.load(f)

# 5. Save or update data into the database
for item in data:
    Disease.objects.update_or_create(
        name=item['name'],
        defaults={
            'symptoms': item.get('symptoms', ''),
            'test_results': item.get('test_results', ''),
            'recommendation': item.get('recommendation', ''),
            'medicine': item.get('medicine', '')
        }
    )

print("✅ Diseases imported or updated successfully.")
