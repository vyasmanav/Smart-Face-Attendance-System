# System Architecture & Facial Recognition Pipeline

## 1. High-Level Architecture Overview

The system is built upon a decoupled client-server pattern optimized for computer vision workloads:

1. **Client Tier**:
   - Web application built with responsive HTML5, modern CSS, and Bootstrap.
   - Client-side face tracking powered by `face-api.js` (TensorFlow.js backend) running locally in the user's browser for instant landmark alignment and real-time bounding boxes.
2. **Application Tier (Backend)**:
   - Python 3.9 + Django 4.1 REST Framework API.
   - Custom JWT authentication middleware ensuring stateless and role-guarded communication.
   - Computer vision service executing `DeepFace` embedding extraction and cosine distance metric computation.
3. **Database Tier**:
   - MongoDB database storing user collections, biometric 128/512-dimension face vectors, course timetables, and date-stamped attendance logs.

---

## 2. Facial Recognition Verification Pipeline

```
[Camera Input] 
      │
      ▼
[Client: face-api.js] ──> (Landmark detection & alignment preview)
      │
      ▼ (Base64 / Multipart Image Stream)
[Backend REST API: /api/attendance/]
      │
      ▼
[MTCNN Face Detector] ──> (Bounding box crop & normalization)
      │
      ▼
[DeepFace Representation] ──> (Extract 128/512-d feature vector)
      │
      ▼
[MongoDB Query] ──> (Fetch registered student embeddings for session)
      │
      ▼
[Cosine Distance Computation] ──> Distance < Threshold (0.40) ?
      ├── YES ──> [Mark Attendance: "PRESENT" + Timestamp Record]
      └── NO  ──> [Reject: "Face mismatch or unregistered student"]
```

---

## 3. Database Schema Design (MongoDB)

- **Users Collection**: User credentials, email, password hash, role (`student`, `faculty`, `college_admin`), active status.
- **Students Collection**: Academic profile, enrollment number, department, semester, reference biometric face vector embedding.
- **Timetable Collection**: Day of week, start time, end time, department, subject, faculty assigned, room.
- **Attendance Collection**: Student reference ID, slot reference ID, date, status (`Present`, `Absent`, `Excused`), verified timestamp, verification confidence score.
- **Queries Collection**: Student reference, query category, question text, status (`Open`, `Answered`), faculty reply text, resolved date.
