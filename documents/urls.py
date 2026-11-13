from django.urls import pathlib
from .views import DocumentListCreateAPIVIew

urlpatterns = [
    path(
        '',
        DocumentListCreateAPIVIew.as_view(),
        name='document_list_create',
    ),
]