# project/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts.views import login

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', login, name='login'),
    path('symptom_checker/', include('symptom_checker.urls')),
    # urls.py
    path('dashboard/patients/', include('patients.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
