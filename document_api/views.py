from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer
from django.contrib.auth.models import User
from .auth_serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated

from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from .resume_parser import (
    extract_email,
    extract_phone,
    extract_name,
    extract_skills
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .ai_summary import generate_resume_summary

# Tesseract Path
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
        document = serializer.save()

        extracted_text = ""

        try:
            file_path = document.file.path

            # PDF OCR
            if file_path.lower().endswith(".pdf"):

                pages = convert_from_path(
                    file_path,
                    poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
                )

                for page in pages:
                    extracted_text += pytesseract.image_to_string(page)
                    extracted_text += "\n"

            # Image OCR
            else:
                image = Image.open(file_path)
                extracted_text = pytesseract.image_to_string(image)

            document.extracted_text = extracted_text
            document.name = extract_name(extracted_text)
            document.email = extract_email(extracted_text)
            document.phone = extract_phone(extracted_text)

            skills = extract_skills(extracted_text)
            document.skills = ", ".join(skills)
            document.summary = generate_resume_summary(
                extracted_text
            )

            document.save()

        except Exception as e:
            print("OCR Error:", e)