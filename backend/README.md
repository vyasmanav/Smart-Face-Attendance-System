# Student Attendance System

## Project Overview
A comprehensive student attendance management system that leverages facial recognition technology to automate and streamline attendance tracking in educational institutions. The system provides different interfaces for students, faculty, and administrators to manage their respective workflows efficiently.

## Features

### Authentication & Authorization
- **User Registration**: Comprehensive signup system with role-based access control
- **User Login**: Secure authentication with JWT token generation
- **Role-Based Access**: Different access levels for students, faculty, and college administrators

### Student Management (Admin)
- **Student Registration**: Add new students to the system
- **Student Profile Management**: Update student information
- **Student Listing**: View all registered students with filtering options
- **Student Removal**: Ability to mark students as deleted

### Attendance System
- **Facial Recognition Attendance**: Automated attendance marking using facial recognition
- **Biometric Data Management**: Students can register and update their biometric data
- **Manual Correction**: Faculty can manually correct attendance records if needed
- **Attendance Reports**: View attendance reports by student, class, or date

### Timetable Management
- **Class Scheduling**: Create and manage class timetables
- **Schedule Viewing**: View scheduled classes and sessions
- **Timetable Customization**: Modify existing schedules as needed

### Query & Support System
- **Student Queries**: Students can raise queries related to attendance or classes
- **Faculty Responses**: Faculty can view and respond to student queries
- **Query Tracking**: Track the status and resolution of queries

## Technical Stack

### Backend
- **Framework**: Django + Django REST Framework
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Facial Recognition**: DeepFace, MTCNN, OpenCV
- **Image Processing**: NumPy, OpenCV

### Dependencies
- Python 3.x
- Django 4.1.5
- Django REST Framework 3.14.0
- DeepFace 0.0.78
- MTCNN 0.1.1
- OpenCV 4.7.0.68
- JWT for authentication
- MongoDB for database
- Other dependencies as listed in requirements.txt

## Project Structure
```
backend/
├── API/                # Main API application
│   ├── views.py        # API endpoints and logic
│   ├── urls.py         # URL routing
│   ├── db.py           # Database configuration
│   ├── utils.py        # Utility functions
│   └── middleware.py   # Custom middleware
├── rest/               # REST framework configuration
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.x
- MongoDB
- Virtual environment (recommended)

### Installation Steps
1. Clone the repository
   ```
   git clone https://github.com/yourusername/student-attendance-system.git
   ```

2. Navigate to the project directory
   ```
   cd student-attendance-system/backend
   ```

3. Create and activate a virtual environment (optional but recommended)
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies
   ```
   pip install -r requirements.txt
   ```

5. Configure MongoDB settings in API/db.py

6. Run migrations
   ```
   python manage.py migrate
   ```

7. Start the development server
   ```
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/signup/` - Register a new user
- `POST /api/login/` - Authenticate a user and get a token

### Student Management
- `GET /api/get-students/` - List all students
- `POST /api/manage-student/<id>/` - Add student details
- `PATCH /api/manage-student/<id>/` - Update student details
- `DELETE /api/manage-student/<id>/` - Delete a student

### Attendance
- `POST /api/attendance/` - Mark attendance using facial recognition
- `GET /api/get-attendance/` - Get attendance records
- `GET /api/get-attendance/<id>/` - Get attendance for a specific student
- `PATCH /api/correct-attendance/<id>/` - Manually correct attendance

### Timetable
- `GET /api/get-timetable/` - View timetable
- `POST /api/manage-timetable/` - Create new timetable
- `PATCH /api/manage-timetable/<id>/` - Update timetable
- `GET /api/get-required-timetable-details/` - Get timetable details

### Queries
- `POST /api/query/` - Submit a query (for students)
- `GET /api/get-queries/` - Get all queries
- `GET /api/get-queries/<id>/` - Get specific query
- `POST /api/answer-query/<id>/` - Answer a query (for faculty)

### Biometrics
- `POST /api/manage-biometrics/` - Register biometric data
- `PATCH /api/manage-biometrics/` - Update biometric data

## License
MIT License

## Contributors
- Add contributors here
