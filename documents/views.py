from rest_framework import generics

from .models import Document
from .serializers import DocumentSerializer

class DocumentListCreateAPIVIew(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

# Create your views here.
