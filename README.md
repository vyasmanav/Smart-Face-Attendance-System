# Smart Face Attendance System 🎓📸

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.1.5-green.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![REST Framework](https://img.shields.io/badge/DRF-3.14.0-red.svg)](https://www.django-rest-framework.org/)
[![DeepFace](https://img.shields.io/badge/DeepFace-0.0.78-orange.svg)](https://github.com/serengil/deepface)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.7.0-purple.svg?logo=opencv&logoColor=white)](https://opencv.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-brightgreen.svg?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, automated **Student Attendance & Institutional Management System** powered by computer vision, deep learning face verification, and role-based access control.

---

## 🌟 Overview

The **Smart Face Attendance System** eliminates manual roll calls and buddy-punching in academic institutions. By combining client-side real-time face detection (via `face-api.js`) and high-accuracy server-side facial embedding verification (via `DeepFace` + `MTCNN` + `OpenCV`), the system delivers instantaneous, spoof-resistant attendance tracking.

The platform provides dedicated, role-specific portals for:
- 👨‍🎓 **Students**: Register biometrics, verify daily attendance, update profile, and raise academic queries.
- 👩‍🏫 **Faculty**: Review automated class attendance, perform manual corrections, and answer student inquiries.
- 🏛️ **College Administrators**: Manage student directories, configure schedules/timetables, and generate comprehensive attendance analytics.

---

## 🚀 Key Features

### 1. Facial Recognition & Biometric Pipeline
- **Dual Verification Architecture**: Lightweight client-side landmark tracking for user feedback paired with deep neural net server verification.
- **Biometric Registration & Updates**: Multi-angle facial capture with automated face vector extraction and MongoDB storage.
- **Spoof & Duplicate Resistance**: Distance threshold validation against registered biometric embeddings.

### 2. Multi-Role Authentication & Security
- **JWT (JSON Web Tokens)**: Stateless authentication with role-based claim validation.
- **Granular Access Control**: Segregated APIs and portals for Students, Faculty, and College Administrators.
- **Secure Password Hashing**: Cryptographically secure credential management.

### 3. Comprehensive Institutional Workflows
- **Timetable & Schedule Management**: Dynamic lecture schedule creation, slot allocation, and classroom tracking.
- **Query & Support Desk**: Interactive student-faculty query ticket pipeline for attendance disputes and academic inquiries.
- **Export & Reporting**: Real-time attendance percentages, deficiency reports, and date-wise filtering.

---

## 🏗️ System Architecture

```
                       +----------------------------------+
                       |    Client Browser / Devices      |
                       |  (HTML5, Bootstrap, face-api.js) |
                       +-----------------+----------------+
                                         |
                                HTTP / REST API (JWT)
                                         |
                                         v
                       +-----------------+----------------+
                       |     Django REST Framework API    |
                       |   (Routing, Auth, Middleware)    |
                       +-----------------+----------------+
                                         |
                +------------------------+------------------------+
                |                                                 |
                v                                                 v
+---------------+----------------+               +----------------+---------------+
|    Computer Vision Engine      |               |        Database Layer          |
|  - MTCNN Face Detection        |               |  - MongoDB Atlas / Local       |
|  - DeepFace Embeddings         |               |  - Student Biometrics Vectors  |
|  - OpenCV Image Normalization  |               |  - Timetable, Attendance, Logs |
+--------------------------------+               +--------------------------------+
```

---

## 📂 Project Structure

```
Smart-Face-Attendance-System/
├── attendance-system-frontend/        # Client-side web application & portals
│   ├── assets/
│   │   ├── css/                       # Bootstrap and custom UI stylesheets
│   │   ├── fonts/                     # Font awesome and web fonts
│   │   ├── images/                    # UI branding, avatars, and assets
│   │   └── js/
│   │       ├── models/                # Pretrained face-api neural net weights
│   │       ├── vendor/                # jQuery, Bootstrap, slick, waypoints
│   │       └── *.js                   # Role-specific client logic controllers
│   ├── college-admin-*.html           # Administrator portal screens
│   ├── faculty-*.html                 # Faculty management screens
│   ├── student-*.html                 # Student self-service screens
│   ├── login.html                     # Central authentication screen
│   └── register.html                  # User onboarding screen
│
├── backend/                           # Django REST Framework backend
│   ├── API/                           # Core service application
│   │   ├── migrations/                # Database migrations
│   │   ├── db.py                      # MongoDB connection & client handler
│   │   ├── middleware.py              # JWT authentication & session parsing
│   │   ├── urls.py                    # API route dispatching
│   │   ├── utils.py                   # Facial recognition & vector utilities
│   │   └── views.py                   # REST controller endpoints
│   ├── rest/                          # Django project configuration (settings, asgi, wsgi)
│   ├── manage.py                      # Django management command script
│   └── requirements.txt               # Backend dependencies
│
├── docker-compose.yml                 # Multi-container local orchestration
├── Dockerfile                         # Backend container specification
├── requirements.txt                   # Root Python dependencies
├── run_backend.bat                    # Quick launcher for Django API server
├── run_frontend.bat                   # Quick launcher for frontend dev server
├── setup.ps1                          # Automated Windows PowerShell environment setup
├── .env.example                       # Environment variables template
├── API_DOCUMENTATION.md               # Complete REST API reference
├── SYSTEM_ARCHITECTURE.md             # Technical architecture & pipeline details
└── README.md                          # Project documentation
```

---

## ⚡ Quickstart Guide

### Prerequisites
- Python 3.9+ installed
- MongoDB installed locally or a [MongoDB Atlas](https://www.mongodb.com/atlas) URI
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/vyasmanav/Smart-Face-Attendance-System.git
cd Smart-Face-Attendance-System
```

### 2. Setup Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `backend/.env` and update the database connection:
```bash
copy .env.example backend\.env
```

### 4. Run Migrations & Start Server
```bash
cd backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### 5. Launch the Frontend
Open `attendance-system-frontend/login.html` in your web browser or serve it using any static server:
```bash
cd attendance-system-frontend
python -m http.server 5500
```
Navigate to `http://localhost:5500/login.html`.

---

## 🔌 API Endpoint Highlights

| Method | Endpoint | Description | Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/signup/` | User account registration | Public |
| `POST` | `/api/login/` | JWT token authentication | Public |
| `POST` | `/api/attendance/` | Submit facial image for attendance verification | Student / Faculty |
| `GET` | `/api/get-attendance/` | Fetch attendance history and percentage metrics | All Authenticated |
| `PATCH` | `/api/correct-attendance/<id>/` | Manual attendance status override | Faculty |
| `POST` | `/api/manage-biometrics/` | Register initial facial embedding vector | Student |
| `PATCH` | `/api/manage-biometrics/` | Update biometric facial reference | Student |
| `GET` | `/api/get-timetable/` | Fetch schedule slots by class/department | All Authenticated |
| `POST` | `/api/manage-timetable/` | Create or update lecture timetable | Admin |
| `POST` | `/api/query/` | Submit query ticket | Student |
| `POST` | `/api/answer-query/<id>/` | Resolve query ticket | Faculty |

*For complete payload and response schemas, refer to [API_DOCUMENTATION.md](API_DOCUMENTATION.md).*

---

## 🐳 Docker Deployment

Run the entire stack with Docker Compose:
```bash
docker-compose up --build
```

---

## 👤 Author & Maintainer

Developed and maintained by:
- **Manav Vyas** ([@vyasmanav](https://github.com/vyasmanav))
- Contact: `manav2306@gmail.com`

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
