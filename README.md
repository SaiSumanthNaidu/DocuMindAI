# 📄 DocuMindAI

AI-powered document processing and OCR platform built using Django, Django REST Framework, Tesseract OCR, and Python.

DocuMindAI extracts structured information from various government documents and invoices and returns clean JSON responses.

---

# 🚀 Features

- Aadhaar Card OCR
- PAN Card OCR
- Voter ID OCR
- Passport OCR
- Driving License OCR
- Invoice/Bill OCR
- Structured JSON Extraction
- OCR Preprocessing
- PDF Support
- Image Support
- JWT Authentication
- REST APIs

---

# 🛠️ Tech Stack

- Python 3.13+
- Django
- Django REST Framework
- SQLite
- Tesseract OCR
- Pillow (PIL)
- pdf2image
- Poppler
- JWT Authentication

---

# 📂 Project Structure

```text
DocuMindAI/
│
├── document_api/
│   ├── parsers/
│   │   ├── aadhaar_parser.py
│   │   ├── pan_parser.py
│   │   ├── voter_parser.py
│   │   ├── passport_parser.py
│   │   ├── dl_parser.py
│   │   └── invoice_parser.py
│   │
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── ocr_utils.py
│   └── document_parser.py
│
├── media/
├── uploads/
├── manage.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation Process

## 1. Clone Repository

```bash
git clone https://github.com/SaiSumanthNaidu/DocuMindAI.git

cd DocuMindAI
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Required Packages

```bash
pip install django
pip install djangorestframework
pip install pillow
pip install pytesseract
pip install pdf2image
pip install djangorestframework-simplejwt
```

---

# 🔍 Tesseract OCR Installation

Download Tesseract:

https://github.com/UB-Mannheim/tesseract/wiki

Install to:

```text
C:\Program Files\Tesseract-OCR\
```

Add inside your code:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

Check installation:

```bash
tesseract --version
```

---

# 📄 Poppler Installation (PDF Support)

Download Poppler:

https://github.com/oschwartz10612/poppler-windows/releases

Extract to:

```text
C:\poppler
```

Example path:

```text
C:\poppler\poppler-26.02.0\Library\bin
```

Usage:

```python
convert_from_path(
    file_path,
    poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
)
```

---

# 🗄 Database Migration

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

---

# 👤 Create Super User

```bash
python manage.py createsuperuser
```

Enter:

- Username
- Email
- Password

---

# ▶️ Run Development Server

```bash
python manage.py runserver
```

Server URL:

```text
http://127.0.0.1:8000/
```

---

# 🔑 JWT Authentication APIs

## Obtain Token

```text
POST /api/token/
```

Body:

```json
{
    "username": "admin",
    "password": "password"
}
```

---

## Refresh Token

```text
POST /api/token/refresh/
```

Body:

```json
{
    "refresh": "refresh_token"
}
```

---

# 📤 Document Upload API

```text
POST /api/documents/
```

Form Data:

| Field | Type |
|------|------|
| title | Text |
| front_file | File |
| back_file | File |

Authorization:

```text
Bearer YOUR_ACCESS_TOKEN
```

---

# 📄 Dashboard API

```text
GET /api/dashboard/
```

Returns:

- Total documents
- Latest document
- Uploaded documents

---

# 🔍 Search API

```text
GET /api/search/?keyword=name
```

---

# 📁 My Documents API

```text
GET /api/mydocuments/
```

---

# ✅ Supported Documents

| Document | Status |
|---------|---------|
| Aadhaar Card | ✅ |
| PAN Card | ✅ |
| Voter ID | ✅ |
| Passport | ✅ |
| Driving License | ✅ |
| Invoice/Bill | ✅ |

---

# 📊 OCR Processing Flow

1. Upload document.
2. Image preprocessing.
3. OCR extraction.
4. Document identification.
5. Parser execution.
6. Structured JSON generation.
7. API response.

---

# 📦 Example Aadhaar Response

```json
{
    "document_type": "Aadhaar Card",
    "name": "Bandaru Sai Sumanth",
    "dob": "01/04/2004",
    "gender": "Male",
    "aadhaar_number": "XXXX XXXX XXXX"
}
```

---

# 📦 Example Invoice Response

```json
{
    "document_type": "Invoice",
    "vendor_name": "Prashanth MultiMart",
    "customer_name": "Bandari Enterprises",
    "invoice_date": "12-03-2026",
    "total_amount": "3470.00"
}
```

---

# 📋 Generate Requirements File

```bash
pip freeze > requirements.txt
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔧 Useful Commands

Check migrations:

```bash
python manage.py showmigrations
```

Create app:

```bash
python manage.py startapp app_name
```

Collect static files:

```bash
python manage.py collectstatic
```

Run shell:

```bash
python manage.py shell
```

---

# 🚀 Future Enhancements

- AI Document Summary
- Document Search Engine
- Dashboard Analytics
- Excel Export
- PDF Export
- Confidence Scores
- Cloud Deployment

---

# 👨‍💻 Author

**Bandaru Sai Sumanth**

GitHub:

https://github.com/SaiSumanthNaidu

---

# 📜 License

This project is developed for educational, research, and portfolio purposes.