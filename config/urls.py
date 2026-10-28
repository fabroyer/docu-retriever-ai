from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

def check(request):
    """Check the health of the application."""
    return JsonResponse({
        "status": "ok",
        "application": "DocuRetriever AI",
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/check/', check, name="check"),
]
