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

from .resume_parser import (
    extract_email,
    extract_phone,
    extract_name,
    extract_skills
)

from .ai_summary import generate_resume_summary
from django.db.models import Q


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

        document = serializer.save(
            user=self.request.user
        )

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

    
class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        documents = Document.objects.filter(
            user=request.user
        )

        latest_resume = None

        if documents.exists():
            latest_resume = documents.last().title

        total_skills = 0

        for doc in documents:
            if doc.skills:
                skills = [
                    skill.strip()
                    for skill in doc.skills.split(",")
                    if skill.strip()
                    ]

            total_skills += len(skills)

        data = {
            "total_resumes": documents.count(),
            "latest_resume": latest_resume,
            "total_skills": total_skills,
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

        skill = self.request.GET.get("skill")
        name = self.request.GET.get("name")

        if skill:
            queryset = queryset.filter(
                skills__icontains=skill
            )

        if name:
            queryset = queryset.filter(
                name__icontains=name
            )

        return queryset

class MyDocumentsView(generics.ListAPIView):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(
            user=self.request.user
        )