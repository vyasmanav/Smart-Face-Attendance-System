# API Documentation - Smart Face Attendance System

All requests expect `Content-Type: application/json` unless uploading multipart/form-data images.
Protected endpoints require the header:
```http
Authorization: Bearer <JWT_TOKEN>
```

---

## 1. Authentication Endpoints

### 1.1 User Signup
- **URL**: `/api/signup/`
- **Method**: `POST`
- **Access**: Public
- **Request Body**:
```json
{
  "username": "student_john",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "role": "student"
}
```
- **Response `201 Created`**:
```json
{
  "message": "User registered successfully",
  "user_id": "64f128ab09c48b0012345678",
  "role": "student"
}
```

### 1.2 User Login
- **URL**: `/api/login/`
- **Method**: `POST`
- **Access**: Public
- **Request Body**:
```json
{
  "username": "student_john",
  "password": "SecurePassword123!"
}
```
- **Response `200 OK`**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "role": "student",
  "user": {
    "username": "student_john",
    "email": "john@example.com"
  }
}
```

---

## 2. Facial Recognition & Biometrics

### 2.1 Biometric Registration
- **URL**: `/api/manage-biometrics/`
- **Method**: `POST`
- **Access**: Student (Authenticated)
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `face_image`: Image file (JPG/PNG)
- **Response `200 OK`**:
```json
{
  "status": "success",
  "message": "Biometric face embedding registered successfully"
}
```

### 2.2 Attendance Verification
- **URL**: `/api/attendance/`
- **Method**: `POST`
- **Access**: Student / Faculty (Authenticated)
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `face_image`: Captured frame image
  - `slot_id`: Scheduled class slot ID
- **Response `200 OK`**:
```json
{
  "status": "verified",
  "student_name": "John Doe",
  "timestamp": "2026-03-27T10:15:00Z",
  "attendance_status": "Present"
}
```

---

## 3. Student Management (Admin)

### 3.1 Get All Students
- **URL**: `/api/get-students/`
- **Method**: `GET`
- **Access**: Admin / Faculty
- **Query Params**: `department`, `year`, `semester`
- **Response `200 OK`**:
```json
{
  "students": [
    {
      "id": "64f128ab09c48b0012345678",
      "name": "John Doe",
      "enrollment_no": "EN2024001",
      "department": "Computer Science",
      "semester": 6
    }
  ]
}
```

---

## 4. Timetable Management

### 4.1 Get Timetable
- **URL**: `/api/get-timetable/`
- **Method**: `GET`
- **Access**: Authenticated

### 4.2 Create / Update Schedule Slot
- **URL**: `/api/manage-timetable/`
- **Method**: `POST`
- **Access**: Admin
- **Request Body**:
```json
{
  "department": "Computer Science",
  "semester": 6,
  "subject": "Deep Learning",
  "faculty": "Dr. Smith",
  "day": "Monday",
  "start_time": "10:00",
  "end_time": "11:00",
  "classroom": "Lab 302"
}
```
