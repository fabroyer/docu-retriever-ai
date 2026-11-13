from rest_framework import generics

from .models import Document
from .serializer import DocumentSerializer

class DocumentListCreateAPIVIew(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

# Create your views here.
