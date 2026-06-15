from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User

from .models import Document
from .serializers import DocumentSerializer
from .auth_serializers import RegisterSerializer

from PIL import Image
import pytesseract
from pdf2image import convert_from_path

from .document_parser import analyze_document


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class DocumentUploadView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):

        document = serializer.save(
            user=self.request.user
        )

        extracted_text = ""

        try:

            file_path = document.file.path

            if file_path.lower().endswith(".pdf"):

                pages = convert_from_path(
                    file_path,
                    poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
                )

                for page in pages:
                    extracted_text += (
                        pytesseract.image_to_string(page)
                        + "\n"
                    )

            else:

                image = Image.open(file_path)

                extracted_text = pytesseract.image_to_string(
                    image
                )

            document.extracted_text = extracted_text

            document.structured_data = analyze_document(
                extracted_text
            )

            document.save()

        except Exception as e:

            print("OCR / AI Error:", str(e))

            document.extracted_text = extracted_text

            document.structured_data = {
                "error": str(e)
            }

            document.save()


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        documents = Document.objects.filter(
            user=request.user
        )

        latest_document = None

        if documents.exists():
            latest_document = documents.last().title

        data = {
            "total_documents": documents.count(),
            "latest_document": latest_document,
            "uploaded_documents": [
                doc.title for doc in documents
            ]
        }

        return Response(data)


class ResumeSearchView(generics.ListAPIView):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Document.objects.filter(
            user=self.request.user
        )

        keyword = self.request.GET.get(
            "keyword"
        )

        if keyword:
            queryset = queryset.filter(
                extracted_text__icontains=keyword
            )

        return queryset


class MyDocumentsView(generics.ListAPIView):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Document.objects.filter(
            user=self.request.user
        )