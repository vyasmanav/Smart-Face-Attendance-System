from django.shortcuts import render
from .utils import create_unique_object_id, pwd_context
from .db import auth_collection, database, fields, jwt_life, jwt_secret
import jwt
import datetime
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
import numpy as np
import json
from rest.settings import FIREBASECONFIG, MEDIA_ROOT
import pyrebase
import os
import base64
from django.core.files.storage import default_storage
import cv2
# from MTCNN import MTCNN
from deepface import DeepFace
from mtcnn import MTCNN
# Create your views here.


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@api_view(["POST"])
def signup(request):
    data = request.data if request.data is not None else {}
    print(data)
    all_fields = fields + ("first_name", "last_name", "date_of_birth", "gender",
                           "contact_number", "address_line_1", "address_line_2", "landmark", "pincode", "role")
    if data != {}:
        data["_id"] = create_unique_object_id()
        for field in all_fields:
            if field in data:
                continue
            else:
                return JsonResponse(data={"message": "Wrong data provided!"}, status=HTTP_400_BAD_REQUEST)
        data["password"] = pwd_context.hash(data["password"])
        if database[auth_collection].find_one({"email": data["email"]}) is None:
            try:
                database[auth_collection].insert_one(data)
                return JsonResponse(data={"message": "User Registered"}, status=HTTP_201_CREATED)
            except:
                return JsonResponse(data={"message": "User not Sign up"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "User Already Exists"}, status=HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={"message": "Didn't receive signup data"}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    data = request.data if request.data is not None else {}
    if data:
        email = data["email"]
        password = data["password"]

        if "@" in email:
            user = database[auth_collection].find_one({"email": email})
        else:
            return JsonResponse(data={"message": "Wrong Email Format"}, status=HTTP_400_BAD_REQUEST)

        if user is not None:
            if pwd_context.verify(password, user["password"]):
                payload = {
                    "id": user["_id"],
                    "role": user["role"],
                    "exp": datetime.datetime.now() + datetime.timedelta(days=jwt_life)
                }
                print(user)
                token = jwt.encode(payload, jwt_secret, algorithm="HS256")
                if type(token) == str:
                    if user["role"] == "admin":
                        return JsonResponse(data={"message": "Successfully Logged In", "token": token, "role": user["role"], "fullname": user["username"]}, status=HTTP_200_OK)
                    else:
                        return JsonResponse(data={"message": "Successfully Logged In", "token": token, "role": user["role"], "fullname": f"{user['first_name']} {user['middle_name']} {user['last_name']}"}, status=HTTP_200_OK)
                else:
                    return JsonResponse(data={"message": "Token not created"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return JsonResponse(data={"message": "Incorrect Password"}, status=HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data={"message": "User not found"}, status=HTTP_404_NOT_FOUND)
    else:
        return JsonResponse(data={"message": "Didn't Receive Login Data"}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def manage_student(request, id):
    if request.method == "POST":
        college_admin = database["User"].find_one(
            filter={"_id": request.id, "role": request.role})
        print(college_admin)
        try:
            if college_admin.get("role").lower() == "college-admin" and college_admin["_id"] == request.id:
                print("access granted")
                data = request.data if request.data is not None else {}
                if id is not None:
                    print(id)
                    user = database["User"].find_one(
                        filter={"_id": id, "role": "Student"})
                    data["_id"] = create_unique_object_id()
                    data["User_ID"] = id
                    student_fields = (
                        "gr_number", "roll_number", "admission_date", "admission_valid_date", "division_id")
                    for field in student_fields:
                        if field in data:
                            continue
                        else:
                            return JsonResponse(data={"message": "Wrong Data Provided"}, status=HTTP_400_BAD_REQUEST)
                    data["is_deleted"] = False
                    database["Student"].insert_one(data)
                    return JsonResponse(data={"message": "User Successfully Inserted"}, status=HTTP_201_CREATED)
                else:
                    return JsonResponse(data={"message": "Didn't receive student data"},status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(data={"message": "You're not Authorized"}, status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "PATCH":
        college_admin = database["User"].find_one(
            filter={"_id": request.id, "role": request.role})
        if college_admin["role"] == "college-admin" and college_admin["_id"] == request.id:
            data = request.data if request.data is not None else {}
            if id is not None and data is not None and data != {}:
                print(id)
                user = database["Student"].find_one(filter={"User_ID": id})
                if user:
                    newValues = {"$set": data}
                    print(newValues)
                    try:
                        database["Student"].update_one(
                            filter={"User_ID": id}, update=newValues)
                        return JsonResponse(data={"message": "Student Updated Successfully"}, status=HTTP_200_OK)
                    except:
                        return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return JsonResponse(data={"message": "Student Not found"}, status=HTTP_404_NOT_FOUND)
            else:
                return JsonResponse(data={"message": "Update Data Didn't received"}, status=HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data={"message": "You're not Authorized"}, status=HTTP_401_UNAUTHORIZED)
    elif request.method == "GET":
        user = database["User"].find_one(
            filter={"_id": request.id, "role": request.role})

        if user["role"] == "college-admin" and user["_id"] == request.id:
            data = database["User"].find(
                filter={"role": "Student", "_id": id})
            data = [i for i in data]
            return JsonResponse(data=data, status=HTTP_200_OK, safe=False)
        else:
            return JsonResponse(data={"message": "User not Authorized"}, status=HTTP_401_UNAUTHORIZED)
    elif request.method == "DELETE":
        user = database["User"].find_one(
            filter={"_id": request.id, "role": request.role})

        if user["role"] == "college-admin" and user["_id"] == request.id:
            database["Student"].update_one(filter={"User_ID": id}, update={
                                           "$set": {"is_deleted": True}})
            return JsonResponse(data={"message": "User deleted"}, status=HTTP_200_OK)
        else:
            return JsonResponse(data={"message": "User not Authorized"}, status=HTTP_401_UNAUTHORIZED)


def get_students(request):
    user = database["User"].find_one(
        filter={"_id": request.id, "role": request.role})

    if user["role"] == "college-admin" and user["_id"] == request.id:
        pipeline = [
            {
                "$lookup": {
                    "from": "User",
                    "localField": "User_ID",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$unwind": {"path": "$user"}
            },
            {
                "$project": {
                    "_id": 1,
                    "gr_number": 1,
                    "roll_number": 1,
                    "user.first_name": 1,
                    "user.last_name": 1,
                    "user.contact_number": 1,
                    "user.email": 1,
                    "user._id": 1,
                    "is_deleted": 1
                }
            },
            {
                "$match": {
                    "is_deleted": {
                        "$ne": True
                    }
                }
            }
        ]
        data = database["Student"].aggregate(pipeline)
        data = list(data)
        return JsonResponse(data=data, status=HTTP_200_OK, safe=False)
    else:
        return JsonResponse(data={"message": "User not Authorized"}, status=HTTP_401_UNAUTHORIZED)


@api_view(["POST", "PATCH"])
def manage_biometrics(request):
    from deepface import DeepFace
    import cv2
    from mtcnn import MTCNN
    import numpy as np
    from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED
    from django.http import JsonResponse
    
    try:
        user = database[auth_collection].find_one(
            filter={"_id": request.id, "role": request.role})
        
        if not user:
            return JsonResponse(data={"message": "User not found"}, status=HTTP_404_NOT_FOUND)
            
        if user["role"] == "Student" and user["_id"] == request.id:
            data = request.data if request.data is not None else {}
            
            # Check if face-image exists in request.FILES
            if "face-image" not in request.FILES:
                return JsonResponse(data={"message": "No face image provided"}, status=HTTP_400_BAD_REQUEST)
                
            image = request.FILES["face-image"]
            
            if data:
                if 'face-image' in data:
                    del data['face-image']
                    
                # Process the image
                try:
                    img = np.fromstring(image.read(), np.uint8)
                    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    detector = MTCNN()
                    face = detector.detect_faces(img)
                    print("face detection")
                    
                    if len(face) == 0:
                        return JsonResponse(data={"message": "Face not found please upload proper image"}, status=HTTP_400_BAD_REQUEST)
                        
                    face_embedding = DeepFace.represent(
                        img, enforce_detection=False, model_name="Facenet512")
                    print("embeddings done")
                    data["face"] = face_embedding[0]["embedding"]
                    
                except Exception as e:
                    print(f"Image processing error: {str(e)}")
                    return JsonResponse(data={"message": f"Error processing image: {str(e)}"}, status=HTTP_400_BAD_REQUEST)
                
                # Get student information
                student = database["Student"].find_one(
                    filter={"User_ID": request.id})
                print(f"Request ID: {request.id}")
                print(f"Student found: {student}")
                
                # If student not found, create a basic student record
                if student is None:
                    # Create a new student record
                    new_student = {
                        "_id": create_unique_object_id(),
                        "User_ID": request.id,
                        "roll_number": f"AUTO-{request.id[:8]}",  # Generate a temporary roll number
                        "is_deleted": False
                    }
                    
                    try:
                        database["Student"].insert_one(new_student)
                        student = new_student
                        print(f"Created new student record: {student}")
                    except Exception as e:
                        print(f"Error creating student record: {str(e)}")
                        return JsonResponse(data={"message": "Failed to create student record. Please contact administrator."}, status=HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Now we should have a student record
                try:
                    student_id = student["_id"]
                    
                    if request.method == "POST":
                        # Check if face data already exists
                        existing_face = database["face_data"].find_one({"student_id": student_id})
                        if existing_face:
                            # Update existing face data
                            update = {
                                "$set": {
                                    "face_data": data["face"]
                                }
                            }
                            database["face_data"].find_one_and_update(
                                filter={"student_id": student_id}, update=update)
                            return JsonResponse(data={"message": "Face data updated successfully"}, status=HTTP_200_OK)
                        else:
                            # Create new face data
                            face_data = {
                                "_id": create_unique_object_id(),
                                "student_id": student_id,
                                "face_data": data["face"]
                            }
                            database["face_data"].insert_one(document=face_data)
                            return JsonResponse(data={"message": "Face registered successfully"}, status=HTTP_201_CREATED)
                    elif request.method == "PATCH":
                        print("update start")
                        update = {
                            "$set": {
                                "face_data": data["face"]
                            }
                        }
                        # Check if face data already exists
                        existing_face = database["face_data"].find_one({"student_id": student_id})
                        if existing_face:
                            database["face_data"].find_one_and_update(
                                filter={"student_id": student_id}, update=update)
                            print("update end")
                            return JsonResponse(data={"message": "Face data updated successfully"}, status=HTTP_200_OK)
                        else:
                            # If face data doesn't exist, create it
                            face_data = {
                                "_id": create_unique_object_id(),
                                "student_id": student_id,
                                "face_data": data["face"]
                            }
                            database["face_data"].insert_one(document=face_data)
                            return JsonResponse(data={"message": "Face registered successfully"}, status=HTTP_201_CREATED)
                except KeyError as e:
                    print(f"KeyError: {str(e)}")
                    return JsonResponse(data={"message": f"Invalid student data structure: {str(e)}"}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(data={"message": "No data provided"}, status=HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data={"message": "User is not Authorized"}, status=HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(f"Error in manage_biometrics: {str(e)}")
        return JsonResponse(data={"message": f"An error occurred: {str(e)}"}, status=HTTP_400_BAD_REQUEST)


i = 1

# original implementation
# @api_view(["POST"])
# def attendance(request, id):
#     if id is not None:
#         pipeline = [
#             {
#                 "$match": {
#                     "_id": {
#                         "$eq": id
#                     }
#                 }
#             },
#             {
#                 "$lookup": {
#                     "from": "subject", 
#                     "localField": "subject_id", 
#                     "foreignField": "_id", 
#                     "as": "subject",
#                 },
#             },
#             {
#                 "$unwind":
#                 {
#                     "path": "$subject",
#                 },
#             },
#             {
#                 "$project": {
#                     "_id": 1,
#                     "subject.subject_name": 1,
#                     "date": 1,
#                 },
#             },
#             {
#                 "$limit": 1
#             }
#         ]

#         lecture = database["timetable"].aggregate(pipeline=pipeline)
#         lecture = [i for i in lecture]
#     else:
#         return JsonResponse(data={"message": "id of the lecture is not given"}, status=HTTP_400_BAD_REQUEST)

#     if lecture is None or lecture == []:
#         return JsonResponse(data={"message": "there is no lecture for given id please double check the given id"}, status=HTTP_404_NOT_FOUND)

#     lecture = lecture[0]
#     print(lecture)
#     from deepface import DeepFace
#     import cv2
#     from mtcnn import MTCNN
#     if request.method == "POST":
#         # image =
#         image = request.FILES["class-frames"]
#         if image:
#             face_data = []
#             img = np.fromstring(image.read(), np.uint8)
#             img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
#             # print(img)
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             # print(img)
#             detector = MTCNN()
#             faces = detector.detect_faces(img)
#             print(len(faces))

#             if len(faces) == 0:
#                 return JsonResponse(data={"message": "Uploaded Image doesn't contains face"}, status=HTTP_400_BAD_REQUEST)

#             try:
#                 firebase = pyrebase.initialize_app(FIREBASECONFIG)
#                 storage = firebase.storage()
#             except:
#                 return JsonResponse(data={"error_message": "Cloud Connection Failed"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

#             # file uploading to firebase

#             for i, file in enumerate(request.FILES.values()):
#                 filename, fileextension = os.path.splitext(file.name)
#                 if fileextension not in [".png", ".jpg", ".jpeg", ".webp"]:
#                     return JsonResponse(data={"error_message": "Given File is not an image"}, status=HTTP_400_BAD_REQUEST)

#                 new_name = f"{lecture['_id']}-{i}{fileextension}"

#                 print(new_name)
#                 file.name = new_name
#                 default_storage.save(new_name, file)
#                 img_path = f"{lecture['date']}/{lecture['subject']['subject_name']}/{new_name}"
#                 print(img_path)
#                 try:
#                     storage.child(img_path).put(f"{MEDIA_ROOT}/{new_name}")
#                     default_storage.delete(new_name)
#                     image_url = storage.child(img_path).get_url(token=None)
#                     print(image_url)
#                 except:
#                     return JsonResponse(data={"error_message": "Cloud Upload failed."}, status=HTTP_500_INTERNAL_SERVER_ERROR)

#             data = {
#                 "_id": create_unique_object_id(),
#                 "lecture_id": lecture['_id'],
#                 "image_url": image_url
#             }

#             print(data)
#             try:
#                 database["attendance_dataset"].insert_one(data)
#             except:
#                 return JsonResponse(data={"error_message": "Internal Server error."}, status=HTTP_500_INTERNAL_SERVER_ERROR)
#             embeddings = []
#             for face in faces:
#                 x, y, w, h = face["box"]
#                 crop = img[y:y+h, x:x+w]
#                 target_embedding = DeepFace.represent(
#                     crop, enforce_detection=False, model_name="Facenet512")
#                 embeddings.append(target_embedding)

#             for embedding in embeddings:

#                 # to find cosine similarity between to faces
#                 pipeline = [
#                     {
#                         "$addFields": {
#                             "target_embedding": embedding[0]["embedding"]
#                         }
#                     },
#                     {
#                         "$project": {
#                             "student_id": 1,
#                             "cos_sim_params": {
#                                 "$reduce": {
#                                     "input": {"$range": [0, {"$size": "$face_data"}]},
#                                     "initialValue": {
#                                         "dot_product": 0,
#                                         "doc_2_sum": 0,
#                                         "target_2_sum": 0
#                                     },
#                                     "in": {
#                                         "$let": {
#                                             "vars": {
#                                                 "doc_elem": {"$arrayElemAt": ["$face_data", "$$this"]},
#                                                 "target_elem":{"$arrayElemAt": ["$target_embedding", "$$this"]}
#                                             },
#                                             "in":{
#                                                 "dot_product": {
#                                                     "$add": [
#                                                         "$$value.dot_product",
#                                                         {"$multiply": [
#                                                             "$$doc_elem", "$$target_elem"]}
#                                                     ]
#                                                 },
#                                                 "doc_2_sum":{
#                                                     "$add": [
#                                                         "$$value.doc_2_sum",
#                                                         {"$pow": [
#                                                             "$$doc_elem", 2]}
#                                                     ]
#                                                 },
#                                                 "target_2_sum":{
#                                                     "$add": [
#                                                         "$$value.target_2_sum",
#                                                         {"$pow": [
#                                                             "$$target_elem", 2]}
#                                                     ]
#                                                 }
#                                             }
#                                         }
#                                     }
#                                 }
#                             }
#                         }
#                     },
#                     {
#                         "$project": {
#                             "_id": 1,
#                             "student_id": 1,
#                             "cos_sim": {
#                                 "$divide": [
#                                     "$cos_sim_params.dot_product",
#                                     {
#                                         "$sqrt": {
#                                             "$multiply": [
#                                                 "$cos_sim_params.doc_2_sum",
#                                                 "$cos_sim_params.target_2_sum"
#                                             ]
#                                         }
#                                     }
#                                 ]
#                             }
#                         }
#                     },
#                     {
#                         "$match": {
#                             "cos_sim": {
#                                 "$gte": 0.5
#                             }
#                         }
#                     },
#                     {
#                         "$sort": {
#                             "cos_sim": -1
#                         }
#                     },
#                     {
#                         "$limit": 1
#                     }
#                 ]
#                 student_details = database["face_data"].aggregate(
#                     pipeline=pipeline)
#                 face_data.append(list(student_details))
#             all_present = []
#             all_student = database["Student"].find()
#             for face in face_data:
#                 if face != []:
#                     student = database["Student"].find_one(
#                         filter={"User_ID": face[0]["student_id"]})
#                     print(face[0]["student_id"])
#                     all_present.append(student)
#             print(all_present,"all_present")
#             present_ids = [i["_id"] if i is not None else None for i in all_present]
#             # print(_ids)
#             all_student = list(all_student)
#             for student in all_student:
#                 if student["_id"] in present_ids:
#                     all_student.remove(student)
#             present_student = all_present
#             absent_student = all_student
#             # for face in face_data:
#             #     for student in all_students:
#             #         instance = {}
#             #         instance["roll_number"] = student["roll_number"]
#             #         instance["_id"] = create_unique_object_id()
#             #         if face[0]["student_id"] == student["_id"]:
#             #             instance["attendance"] = True
#             #             present_student.append(instance)
#             absent_ids = [i["_id"] for i in absent_student]
#             absent_student = []
#             # for i in absent_ids:
#             #     if i in present_ids:
#             #         absent_ids.remove(i)

#             present_ids = set(present_ids)
#             absent_ids = set(absent_ids)

#             absent_ids = list(absent_ids - present_ids)
#             for absent in absent_ids:
#                 # absent_student.append(list(database["Student"].find_one({"_id":absent},{"_id":1,"roll_number":1})))
#                 student = database["Student"].find_one(
#                     {"_id": absent}, {"_id": 1, "roll_number": 1, 'User_ID': 1})
#                 absent_student.append(student)
#             present_student = []
#             for present in present_ids:
#                 student = database["Student"].find_one(
#                     {"_id": present}, {"_id": 1, "roll_number": 1, 'User_ID': 1})
#                 present_student.append(student)
            
#             # present_absent_data = present_student + absent_student
#             print(all_present)
#             instances = []
#             for present in present_student:
#                 if present:
#                     instance = {}
#                     instance["_id"] = create_unique_object_id()
#                     instance["student_id"] = present.get("_id")
#                     instance["roll_number"] = present.get("roll_number")
#                     instance["attendance"] = True
#                     instance["lecture_id"] = lecture["_id"]
#                     instances.append(instance)
#             for absent in absent_student:
#                 if absent:
#                     instance = {}
#                     instance["_id"] = create_unique_object_id()
#                     instance["student_id"] = absent.get("_id")
#                     instance["roll_number"] = absent.get("roll_number")
#                     instance["attendance"] = False
#                     instance["lecture_id"] = lecture["_id"]
#                 instances.append(instance)

#             try:
#                 database["attendance"].insert_many(instances)
#                 return JsonResponse(data={"present": present_student, "absent": absent_student,"message":"successfully taken the attendance"}, status=HTTP_200_OK)
#             except:
#                 return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return JsonResponse(data={"message": "Image not Found"}, status=HTTP_400_BAD_REQUEST)

# test implementation v1 face recognition working but attendance mechanism not
@api_view(["POST"])
def attendance(request, id):
    from deepface import DeepFace
    import cv2
    from mtcnn import MTCNN
    if id is not None:
        pipeline = [
            {
                "$match": {
                    "_id": {
                        "$eq": id
                    }
                }
            },
            {
                "$lookup": {
                    "from": "subject", 
                    "localField": "subject_id", 
                    "foreignField": "_id", 
                    "as": "subject",
                },
            },
            {
                "$unwind":
                {
                    "path": "$subject",
                },
            },
            {
                "$project": {
                    "_id": 1,
                    "subject.subject_name": 1,
                    "date": 1,
                },
            },
            {
                "$limit": 1
            }
        ]

        lecture = database["timetable"].aggregate(pipeline=pipeline)
        lecture = [i for i in lecture]
    else:
        return JsonResponse(data={"message": "id of the lecture is not given"}, status=HTTP_400_BAD_REQUEST)

    if lecture is None or lecture == []:
        return JsonResponse(data={"message": "there is no lecture for given id please double check the given id"}, status=HTTP_404_NOT_FOUND)

    lecture = lecture[0]
    print(lecture)
    
    if request.method == "POST":
        image = request.FILES.get("class-frames")
        if image:
            try:
                # Read image file
                img = np.fromstring(image.read(), np.uint8)
                img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Face detection using MTCNN
                detector = MTCNN()
                faces = detector.detect_faces(img)
                print(f"Number of faces detected: {len(faces)}")

                if len(faces) == 0:
                    return JsonResponse(data={"message": "Uploaded Image doesn't contain any faces"}, status=HTTP_400_BAD_REQUEST)

                # Initialize Firebase storage
                try:
                    firebase = pyrebase.initialize_app(FIREBASECONFIG)
                    storage = firebase.storage()
                except Exception as e:
                    print(f"Firebase initialization error: {str(e)}")
                    return JsonResponse(data={"error_message": "Cloud Connection Failed"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

                # Upload file to Firebase storage
                image_url = None
                for i, file in enumerate(request.FILES.values()):
                    filename, fileextension = os.path.splitext(file.name)
                    if fileextension.lower() not in [".png", ".jpg", ".jpeg", ".webp"]:
                        return JsonResponse(data={"error_message": "Given File is not an image"}, status=HTTP_400_BAD_REQUEST)

                    new_name = f"{lecture['_id']}-{i}{fileextension}"
                    print(f"New filename: {new_name}")
                    
                    file.name = new_name
                    default_storage.save(new_name, file)
                    img_path = f"{lecture['date']}/{lecture['subject']['subject_name']}/{new_name}"
                    
                    try:
                        storage.child(img_path).put(f"{MEDIA_ROOT}/{new_name}")
                        default_storage.delete(new_name)
                        image_url = storage.child(img_path).get_url(token=None)
                        print(f"Image URL: {image_url}")
                    except Exception as e:
                        print(f"Cloud upload error: {str(e)}")
                        return JsonResponse(data={"error_message": "Cloud Upload failed."}, status=HTTP_500_INTERNAL_SERVER_ERROR)

                # Create attendance dataset record
                data = {
                    "_id": create_unique_object_id(),
                    "lecture_id": lecture['_id'],
                    "image_url": image_url
                }

                print(f"Attendance dataset: {data}")
                try:
                    database["attendance_dataset"].insert_one(data)
                except Exception as e:
                    print(f"Database insertion error: {str(e)}")
                    return JsonResponse(data={"error_message": "Internal Server error."}, status=HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Extract face embeddings using DeepFace with Facenet512
                embeddings = []
                for face in faces:
                    try:
                        x, y, w, h = face["box"]
                        if x < 0: x = 0
                        if y < 0: y = 0
                        # Ensure crop coordinates are valid
                        if y+h <= img.shape[0] and x+w <= img.shape[1]:
                            crop = img[y:y+h, x:x+w]
                            # Get embedding with Facenet512
                            target_embedding = DeepFace.represent(
                                crop, 
                                enforce_detection=False, 
                                detector_backend="skip",  # Skip detection as we already detected
                                model_name="Facenet512"
                            )
                            embeddings.append(target_embedding)
                    except Exception as e:
                        print(f"Error extracting face embedding: {str(e)}")
                        continue

                if not embeddings:
                    return JsonResponse(data={"message": "Could not extract any valid face embeddings"}, status=HTTP_400_BAD_REQUEST)
                
                # Process embeddings for attendance
                face_data = []
                for embedding in embeddings:
                    # Prepare embedding for database query
                    # Handle different embedding formats that DeepFace might return
                    if isinstance(embedding, list) and isinstance(embedding[0], dict) and 'embedding' in embedding[0]:
                        embedding_vector = embedding[0]['embedding']
                    else:
                        embedding_vector = embedding
                    
                    # MongoDB pipeline for cosine similarity calculation
                    pipeline = [
                        {
                            "$addFields": {
                                "target_embedding": embedding_vector
                            }
                        },
                        {
                            "$project": {
                                "student_id": 1,
                                "cos_sim_params": {
                                    "$reduce": {
                                        "input": {"$range": [0, {"$size": "$face_data"}]},
                                        "initialValue": {
                                            "dot_product": 0,
                                            "doc_2_sum": 0,
                                            "target_2_sum": 0
                                        },
                                        "in": {
                                            "$let": {
                                                "vars": {
                                                    "doc_elem": {"$arrayElemAt": ["$face_data", "$$this"]},
                                                    "target_elem":{"$arrayElemAt": ["$target_embedding", "$$this"]}
                                                },
                                                "in":{
                                                    "dot_product": {
                                                        "$add": [
                                                            "$$value.dot_product",
                                                            {"$multiply": [
                                                                "$$doc_elem", "$$target_elem"]}
                                                        ]
                                                    },
                                                    "doc_2_sum":{
                                                        "$add": [
                                                            "$$value.doc_2_sum",
                                                            {"$pow": [
                                                                "$$doc_elem", 2]}
                                                        ]
                                                    },
                                                    "target_2_sum":{
                                                        "$add": [
                                                            "$$value.target_2_sum",
                                                            {"$pow": [
                                                                "$$target_elem", 2]}
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        {
                            "$project": {
                                "_id": 1,
                                "student_id": 1,
                                "cos_sim": {
                                    "$divide": [
                                        "$cos_sim_params.dot_product",
                                        {
                                            "$sqrt": {
                                                "$multiply": [
                                                    "$cos_sim_params.doc_2_sum",
                                                    "$cos_sim_params.target_2_sum"
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        },
                        {
                            "$match": {
                                "cos_sim": {
                                    "$gte": 0.5  # Similarity threshold
                                }
                            }
                        },
                        {
                            "$sort": {
                                "cos_sim": -1
                            }
                        },
                        {
                            "$limit": 1
                        }
                    ]
                    
                    student_details = database["face_data"].aggregate(pipeline=pipeline)
                    face_data.append(list(student_details))
                
                # Process attendance records
                all_present = []
                all_student = database["Student"].find()
                
                for face in face_data:
                    if face != []:
                        student = database["Student"].find_one(
                            filter={"_id": face[0]["student_id"]})
                        print(f"Present student ID: {face[0]['student_id']}")
                        if student:
                            all_present.append(student)
                
                print(f"All present: {all_present}")
                present_ids = [i["_id"] if i is not None else None for i in all_present]
                all_student = list(all_student)
                
                # Find absent students
                for student in all_student[:]:  # Use slice to create a copy for iteration
                    if student["_id"] in present_ids:
                        all_student.remove(student)
                
                present_student = all_present
                absent_student = all_student
                absent_ids = [i["_id"] for i in absent_student]
                
                # Create sets for efficient difference operation
                present_ids = set(present_ids)
                absent_ids = set(absent_ids)
                absent_ids = list(absent_ids - present_ids)
                
                # Get details of absent students
                absent_student = []
                for absent in absent_ids:
                    student = database["Student"].find_one(
                        {"_id": absent}, {"_id": 1, "roll_number": 1, 'User_ID': 1})
                    if student:
                        absent_student.append(student)
                
                # Get details of present students
                present_student = []
                for present in present_ids:
                    student = database["Student"].find_one(
                        {"_id": present}, {"_id": 1, "roll_number": 1, 'User_ID': 1})
                    if student:
                        present_student.append(student)
                
                # Create attendance records
                instances = []
                for present in present_student:
                    if present:
                        instance = {
                            "_id": create_unique_object_id(),
                            "student_id": present.get("_id"),
                            "roll_number": present.get("roll_number"),
                            "attendance": True,
                            "lecture_id": lecture["_id"]
                        }
                        instances.append(instance)
                
                for absent in absent_student:
                    if absent:
                        instance = {
                            "_id": create_unique_object_id(),
                            "student_id": absent.get("_id"),
                            "roll_number": absent.get("roll_number"),
                            "attendance": False,
                            "lecture_id": lecture["_id"]
                        }
                        instances.append(instance)
                
                # Save attendance records to database
                try:
                    if instances:
                        database["attendance"].insert_many(instances)
                    return JsonResponse(
                        data={
                            "present": present_student, 
                            "absent": absent_student, 
                            "message": "Successfully taken the attendance"
                        }, 
                        status=HTTP_200_OK
                    )
                except Exception as e:
                    print(f"Error saving attendance records: {str(e)}")
                    return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return JsonResponse(data={"message": f"Error processing image: {str(e)}"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "Image not Found"}, status=HTTP_400_BAD_REQUEST)


def get_timetable_by_date(request):
    user = database["User"].find_one(
        filter={"_id": request.id, "role": request.role})
    if user["role"].lower() == "college-admin" and user["_id"] == request.id:
        date = request.GET["date"]
        print(date,"====date")
        pipeline = [
    {
        '$lookup': {
            'from': 'subject', 
            'localField': 'subject_id', 
            'foreignField': '_id', 
            'as': 'subject'
        }
    }, {
        '$unwind': {
            'path': '$subject'
        }
    }, {
        '$match': {
            'date': date
        }
    }, {
        '$lookup': {
            'from': 'attendance_dataset', 
            'localField': '_id', 
            'foreignField': 'lecture_id', 
            'as': 'image'
        }
    }, {
        '$unwind': {
            'path': '$image',
            'preserveNullAndEmptyArrays': True
        }
    }, {
        '$project': {
            '_id': 1, 
            'subject.subject_name': 1, 
            'date': 1, 
            'image.image_url': 1
        }
    }
]
        data = database["timetable"].aggregate(pipeline)
        data = list(data)
        return JsonResponse(data=data, status=HTTP_200_OK, safe=False)
    else:
        return JsonResponse(data={"message": "User not Authorized"}, status=HTTP_401_UNAUTHORIZED)


def get_timetable(request):
    user = database["User"].find_one(
        filter={"_id": request.id, "role": request.role})
    if user["role"].lower() == "college-admin" and user["_id"] == request.id:
        pipeline = [
            {
                "$lookup": {
                    "from": "subject",
                    "localField": "subject_id",
                    "foreignField": "_id",
                    "as": "subject"
                }
            },
            {
                "$lookup": {
                    "from": "User",
                    "localField": "faculty_id",
                    "foreignField": "_id",
                    "as": "faculty"
                }
            },
            {
                "$lookup": {
                    "from": "semester",
                    "localField": "semester_id",
                    "foreignField": "_id",
                    "as": "semester"
                }
            },
            {
                "$lookup": {
                    "from": "division",
                    "localField": "division",
                    "foreignField": "_id",
                    "as": "division"
                }
            },
            {"$unwind": "$subject"},
            {"$unwind": "$faculty"},
            {"$unwind": "$division"},
            {"$unwind": "$semester"},
            {
                "$project": {
                    "_id": 1,
                    "remarks": 1,
                    "room_number": 1,
                    "start_time": 1,
                    "end_time": 1,
                    "faculty.first_name": 1,
                    "faculty.last_name": 1,
                    "semester.semester_name": 1,
                    "division.division_name": 1,
                    "subject.subject_name": 1,
                    "date": 1
                }
            }
        ]
        data = database["timetable"].aggregate(pipeline)
        data = list(data)
        return JsonResponse(data=data, status=HTTP_200_OK, safe=False)
    else:
        return JsonResponse(data={"message": "User not Authorized"}, status=HTTP_401_UNAUTHORIZED)


def get_answer(request):
    user = database["User"].find_one(
        filter={"_id": request.id, "role": request.role})
    print(user['role'])
    if user["role"].lower() == "student" and user["_id"] == request.id:

        pipeline = [
            {
                "$lookup": {
                    "from": "query_answer",
                    "localField": "_id",
                    "foreignField": "query_id",
                    "as": "answer"
                }
            },
            {
                "$unwind": "$answer"
            },
            {
                "$lookup": {
                    "from": "User",
                    "localField": "answer.faculty_id",
                    "foreignField": "_id",
                    "as": "faculty"
                }
            },
            {
                "$unwind": "$faculty"
            },
            {
                "$project": {
                    "_id": 1,
                    "faculty.first_name": 1,
                    "faculty.last_name": 1,
                    "query": 1,
                    "answer.answer_of_query": 1
                }
            }
        ]
        data = database["query"].aggregate(pipeline)
        data = [i for i in data]
        return JsonResponse(data=data, status=HTTP_200_OK, safe=False)
    else:
        return JsonResponse(data={"message": "User not Authorized"}, status=HTTP_401_UNAUTHORIZED)


def get_queries(request, id=None):
    user = database["User"].find_one(
        filter={"_id": request.id, "role": request.role})
    if user["role"] == "Faculty" and user["_id"] == request.id:

        if id is not None:
            query = database["query"].find_one({"_id": id}, {"query": 1})
            query = dict(query)
            print(query)
            return JsonResponse(query, status=HTTP_200_OK, safe=False)

        pipeline = [
            {
                "$lookup": {
                    "from": "Student",
                    "localField": "student_id",
                    "foreignField": "_id",
                    "as": "student"
                }
            },
            {"$unwind": "$student"},
            {
                "$lookup": {
                    "from": "User",
                    "localField": "student.User_ID",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {"$unwind": "$user"},
            {
                "$project": {
                    "_id": 1,
                    "query": 1,
                    "query_raised_date": 1,
                    "student.gr_number": 1,
                    "student.roll_number": 1,
                    "user.first_name": 1,
                    "user.last_name": 1,
                    "user.email": 1
                }
            }
        ]
        data = database["query"].aggregate(pipeline)
        data = [i for i in data]
        return JsonResponse(data=data, status=HTTP_200_OK, safe=False)
    else:
        return JsonResponse(data={"message": "User not Authorized"}, status=HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def query(request):
    user = database["User"].find_one(
        filter={"_id": request.id, "role": request.role})
    if user["role"] == "Student" and user["_id"] == request.id:
        data = request.data if request.data else {}
        if data:
            if "query" not in data:
                return JsonResponse(data={"message": "Wrong Data Provided!"}, status=HTTP_400_BAD_REQUEST)
            date = datetime.datetime.now()
            student_details = database["Student"].find_one(
                {"User_ID": user["_id"]}, {"_id": 1})
            print(student_details)
            if student_details is None:
                return JsonResponse(data={"message": "Student details not found. Please check your registration."}, status=HTTP_404_NOT_FOUND)
            query_data = {
                "_id": create_unique_object_id(),
                "student_id": student_details["_id"],
                "query": data["query"],
                "query_raised_date": f"{date.day}-{date.month}-{date.year}"
            }
            print(query_data)
            try:
                database["query"].insert_one(query_data)
                return JsonResponse(data={"message": "Query Successfully Submitted"}, status=HTTP_200_OK)
            except:
                return JsonResponse(data={"message": "Internal Server Erorr"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "No Data Provided"}, status=HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={"message": "User Not Authorized"}, status=HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def answer_query(request, id):
    user = database[auth_collection].find_one(
        filter={"_id": request.id, "role": request.role})

    if user["role"] == "Faculty" and user["_id"] == request.id:
        data = request.data if request.data else {}
        if data:
            if "answer" not in data:
                return JsonResponse(data={"message": "Wrong Data Provided!"}, status=HTTP_400_BAD_REQUEST)
            date = datetime.datetime.now()
            answer_data = {
                "_id": create_unique_object_id(),
                "query_id": id,
                "faculty_id": user["_id"],
                "answer_of_query": data["answer"],
                "query_resolved_data": f"{date.day}-{date.month}-{date.year}"
            }
            try:
                database["query_answer"].insert_one(answer_data)
                return JsonResponse(data={"message": "Answer Successfully Submitted!"}, status=HTTP_201_CREATED)
            except:
                return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "No Data Provided"}, status=HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={"message": "User Not Authorized"}, status=HTTP_401_UNAUTHORIZED)


@api_view(["POST", "PATCH", "DELETE"])
def manage_timetable(request, id=None):
    user = database[auth_collection].find_one(
        filter={"_id": request.id, "role": request.role})
    all_fields = ("subject_id", "faculty_id", "division",
                  "semester_id", "remarks", "room_number", "start_time", "end_time", "date")
    if user["role"] == "college-admin" and user["_id"] == request.id:
        data = request.data if request.data else {}

        if request.method == "DELETE":
            try:
                database["timetable"].update_one(
                    filter={"_id": id}, update={"$set": {"is_deleted": True}})
                return JsonResponse(data={"message": "Successfully Deleted"}, status=HTTP_200_OK)
            except:
                return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        if data:
            for field in data.keys():
                if field not in all_fields:
                    return JsonResponse(data={"message": "Wrong Data Provided"}, status=HTTP_400_BAD_REQUEST)

            if request.method == "POST":
                # required for all fields
                for field in all_fields:
                    if field not in data:
                        return JsonResponse(data={"message": "Wrong Data Provided"}, status=HTTP_400_BAD_REQUEST)

                timetable_data = {
                    "_id": create_unique_object_id(),
                    "subject_id": data["subject_id"],
                    "faculty_id": data["faculty_id"],
                    "semester_id": data["semester_id"],
                    "division": data["division"],
                    "remarks": data["remarks"],
                    "room_number": data["room_number"],
                    "start_time": data["start_time"],
                    "end_time": data["end_time"],
                    "date": data["date"]
                }

                try:
                    database["timetable"].insert_one(timetable_data)
                    return JsonResponse(data={"message": "Timetable Successfully Created"}, status=HTTP_201_CREATED)
                except:
                    return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            elif request.method == "PATCH":

                try:
                    database["timetable"].find_one_and_update(
                        filter={"_id": id}, update={"$set": data})
                    return JsonResponse(data={"message": "Timetable Successfully Updated"}, status=HTTP_201_CREATED)
                except:
                    return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "No Data Provided"}, status=HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={"message": "User Not Authorized"}, status=HTTP_401_UNAUTHORIZED)


def get_attendance(request):
    user = database[auth_collection].find_one(
        filter={"_id": request.id, "role": request.role})
    if user["role"] == "Faculty" and user["_id"] == request.id:
        pipeline = [
            {
                "$lookup": {
                    'from': 'Student',
                    'localField': 'student_id',
                    'foreignField': '_id',
                    'as': 'student_details'
                }
            },
            {"$unwind": "$student_details"},
            {
                "$lookup": {
                    'from': 'User',
                    'localField': 'student_details.User_ID',
                    'foreignField': '_id',
                    'as': 'user'
                }
            },
            {"$unwind": "$user"},
            {
                "$project": {
                    "_id": 1,
                    "roll_number": 1,
                    "attendance": 1,
                    "student_details.gr_number": 1,
                    "student_details.roll_number": 1,
                    "user.first_name": 1,
                    "user.last_name": 1
                }
            },
            {
                "$match": {
                    "attendance": {
                        "$eq": False
                    }
                }
            },
            {
                "$sort": {
                    "roll_number": 1
                }
            }
        ]

        attendance_details = database["attendance"].aggregate(pipeline)
        attendance_details = list(attendance_details)
        return JsonResponse(data=attendance_details, status=HTTP_200_OK, safe=False)
    elif user["role"] == "Student":
        student_details = database["Student"].find_one(
            {"User_ID": user["_id"]}, {"_id": 1})
        print(student_details)
        if student_details is None:
            return JsonResponse(data={"message": "Student details not found. Please check your registration."}, status=HTTP_404_NOT_FOUND)
        pipeline = [
            {
                "$match": {
                    "student_id": student_details["_id"]
                }
            },
            {
                "$lookup": {
                    "from": "timetable",
                    "localField": "lecture_id",
                    "foreignField": "_id",
                    "as": "lecture"
                }
            },
            {
                "$unwind": "$lecture"
            },
            {
                "$lookup": {
                    "from": "subject",
                    "localField": "lecture.subject_id",
                    "foreignField": "_id",
                    "as": "subject"
                }
            },
            {
                "$unwind": "$subject"
            },
            {
                "$project": {
                    "_id": 1,
                    "attendance": 1,
                    "lecture.subject_id": 1,
                    "lecture._id": 1,
                    "subject.subject_name": 1
                }
            },
            {
                "$group": {
                    "_id": "$subject.subject_name",
                    "count": {"$sum": 1}
                }
            }
        ]
        attendance_details = database["attendance"].aggregate(pipeline)

        attendance_details = [i for i in attendance_details]
        return JsonResponse(data=attendance_details, status=HTTP_200_OK, safe=False)
    else:
        return JsonResponse(data={"message": "User Not Authorized"}, status=HTTP_400_BAD_REQUEST)


def correct_attendance(request, id):
    user = database[auth_collection].find_one(
        filter={"_id": request.id, "role": request.role})
    if user["role"] == "Faculty" and user["_id"] == request.id:
        if id:
            database["attendance"].update_one(
                filter={"_id": id, "attendance": False}, update={"$set": {"attendance": True}})
            return JsonResponse(data={"message": "Attendance Updated Successfully"}, status=HTTP_200_OK)
        else:
            return JsonResponse(data={"message": "ID not provided"}, status=HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={"message": "User Not Authorized"}, status=HTTP_401_UNAUTHORIZED)


def required_timetable_details(request):
    user = database[auth_collection].find_one(
        filter={"_id": request.id, "role": request.role})

    if user["role"] == "college-admin" and user["_id"] == request.id:
        semester_details = list(database["semester"].find())
        faculty_details = list(database["User"].find({"role": "Faculty"}, {
                               "_id": 1, "first_name": 1, "last_name": 1}))
        subject_details = list(database["subject"].find(
            {}, {"_id": 1, "subject_name": 1, "subject_type": 1}))
        division_details = list(database["division"].find())
        data = {
            "semester_details": semester_details,
            "faculty_details": faculty_details,
            "subject_details": subject_details,
            "division_details": division_details
        }
        return JsonResponse(data=data, status=HTTP_200_OK)
    else:
        return JsonResponse(data={"message": "User not Authorized"}, status=HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def list_timetables(request):
    """
    List all timetables with subject names and IDs
    """
    try:
        # Aggregate query to join timetable with subject collection
        pipeline = [
            {
                "$lookup": {
                    "from": "subject",
                    "localField": "subject_id",
                    "foreignField": "_id",
                    "as": "subject_details"
                }
            },
            {
                "$unwind": "$subject_details"
            },
            {
                "$project": {
                    "_id": 1,
                    "subject_id": 1,
                    "subject_name": "$subject_details.subject_name",
                    "faculty_id": 1,
                    "division": 1,
                    "semester_id": 1,
                    "room_number": 1,
                    "start_time": 1,
                    "end_time": 1,
                    "date": 1,
                    "subject_details":1
                }
            }
        ]
        
        timetables = list(database["timetable"].aggregate(pipeline))
        
        return JsonResponse(data={"timetables": timetables}, status=HTTP_200_OK)
    except Exception as e:
        return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def add_new_admin(request):
    all_fields = ("username", "email", "password")
    if request.method == "POST":
        data = request.data if request.data else {}
        if data:
            for field in all_fields:
                if field not in data:
                    return JsonResponse(data={"message": "Wrong Data Provided"}, status=HTTP_400_BAD_REQUEST)

            data["password"] = pwd_context.hash(data["password"])

            admin_data = {
                "_id": create_unique_object_id(),
                "username": data["username"],
                "email": data["email"],
                "password": data["password"],
                "role": "admin"
            }

            try:
                database[auth_collection].insert_one(admin_data)
                return JsonResponse(data={"message": "Admin Successfully Added"}, status=HTTP_201_CREATED)
            except:
                return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "No Data Provided"}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST", "PATCH", "GET", "DELETE"])
def manage_faculty(request, id=None):
    user = database[auth_collection].find_one(
        {"_id": request.id, "role": request.role})
    if user["role"] == "admin" and user["_id"] == request.id:
        all_fields = ("first_name", "middle_name", "last_name", "contact_number",
                      "address_line_1", "address_line_2", "landmark", "pincode", "password", "email")
        if request.method == "DELETE":
            try:
                database[auth_collection].update_one(filter={"_id": id}, update={
                                              "$set": {"is_deleted": True}})
                return JsonResponse(data={"message": "Successfully Deleted"}, status=HTTP_200_OK)
            except:
                return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == "GET":
            if id is None:
                faculties = database[auth_collection].find(
                    {"role": "Faculty", "is_deleted": False})
                faculties = list(faculties)
                return JsonResponse(data={"faculties": faculties}, status=HTTP_200_OK)
            elif id is not None:
                faculties = database[auth_collection].find_one(
                    {"_id": id, "role": "Faculty", "is_deleted": False})
                return JsonResponse(data={"faculty": faculties}, status=HTTP_200_OK)
        data = request.data if request.data else {}
        if data:
            for field in data.keys():
                if field not in all_fields:
                    return JsonResponse(data={"message": "Wrong Data Provided"}, status=HTTP_400_BAD_REQUEST)

            if request.method == "POST":
                if database[auth_collection].find_one({"email": data["email"]}) is None:

                    faculty_data = {
                        "_id": create_unique_object_id(),
                        "first_name": data["first_name"],
                        "middle_name": data["middle_name"],
                        "last_name": data["last_name"],
                        "contact_number": data["contact_number"],
                        "address_line_1": data["address_line_1"],
                        "address_line_2": data["address_line_2"],
                        "landmark": data["landmark"],
                        "pincode": data["pincode"],
                        "role": "Faculty",
                        "is_deleted": False
                    }

                    try:
                        database[auth_collection].insert_one(faculty_data)
                        return JsonResponse(data={"message": "Faculty Successfully Inserted"}, status=HTTP_201_CREATED)
                    except:
                        return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return JsonResponse(data={"message": "User Already Exists"}, status=HTTP_400_BAD_REQUEST)
            elif request.method == "PATCH":
                try:
                    database[auth_collection].find_one_and_update(
                        filter={"_id": id}, update={"$set": data})
                    return JsonResponse(data={"message": "Faculty Successfully Updated"}, status=HTTP_200_OK)
                except:
                    return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "No Data Provided"}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST", "PATCH", "GET", "DELETE"])
def manage_college_admin(request, id=None):
    user = database[auth_collection].find_one(
        {"_id": request.id, "role": request.role})
    if user["role"] == "admin" and user["_id"] == request.id:
        all_fields = ("first_name", "middle_name", "last_name", "contact_number",
                      "address_line_1", "address_line_2", "landmark", "pincode", "password", "email")
        if request.method == "DELETE":
            try:
                database[auth_collection].update_one(filter={"_id": id}, update={
                                              "$set": {"is_deleted": True}})
                return JsonResponse(data={"message": "Successfully Deleted"}, status=HTTP_200_OK)
            except:
                return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == "GET":
            if id is None:
                college_admins = database[auth_collection].find(
                    {"role": "college-admin", "is_deleted": False})
                college_admins = list(college_admins)
                return JsonResponse(data={"college_admins": college_admins}, status=HTTP_200_OK)
            elif id is not None:
                college_admins = database[auth_collection].find_one(
                    {"_id": id, "role": "college-admin", "is_deleted": False})
                return JsonResponse(data={"college_admins": college_admins}, status=HTTP_200_OK)
        data = request.data if request.data else {}
        if data:
            for field in data.keys():
                if field not in all_fields:
                    return JsonResponse(data={"message": "Wrong Data Provided"}, status=HTTP_400_BAD_REQUEST)

            if request.method == "POST":
                if database[auth_collection].find_one({"email": data["email"]}) is None:

                    college_admin_data = {
                        "_id": create_unique_object_id(),
                        "first_name": data["first_name"],
                        "middle_name": data["middle_name"],
                        "last_name": data["last_name"],
                        "contact_number": data["contact_number"],
                        "address_line_1": data["address_line_1"],
                        "address_line_2": data["address_line_2"],
                        "landmark": data["landmark"],
                        "pincode": data["pincode"],
                        "role": "college-admin",
                        "is_deleted": False
                    }

                    try:
                        database[auth_collection].insert_one(
                            college_admin_data)
                        return JsonResponse(data={"message": "College Admin Successfully Inserted"}, status=HTTP_201_CREATED)
                    except:
                        return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return JsonResponse(data={"message": "User Already Exists"}, status=HTTP_400_BAD_REQUEST)
            elif request.method == "PATCH":
                try:
                    database[auth_collection].find_one_and_update(
                        filter={"_id": id}, update={"$set": data})
                    return JsonResponse(data={"message": "College Admin Successfully Updated"}, status=HTTP_200_OK)
                except:
                    return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "No Data Provided"}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST", "PATCH", "GET", "DELETE"])
def manage_course(request, id=None):
    user = database[auth_collection].find_one(
        filter={"_id": request.id, "role": request.role})
    if user["role"] == "admin" and user["_id"] == request.id:
        data = request.data if request.data else {}

        if request.method == "DELETE":
            try:
                database["course"].update_one(filter={"_id": id}, update={
                                              "$set": {"is_deleted": True}})
                return JsonResponse(data={"message": "Successfully Deleted"}, status=HTTP_200_OK)
            except:
                return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == "GET":
            courses = database["course"].find({"is_deleted": False})
            courses = list(courses)
            return JsonResponse(data={"courses": courses}, status=HTTP_200_OK)

        if data:
            for field in data.keys():
                if field not in ("course_name", "number_of_semester"):
                    return JsonResponse(data={"message": "Wrong Data Provided"}, status=HTTP_400_BAD_REQUEST)

            if request.method == "POST":
                course_data = {
                    "_id": create_unique_object_id(),
                    "course_name": data["course_name"],
                    "number_of_semester": data["number_of_semester"],
                    "is_deleted": False
                }

                try:
                    database["course"].insert_one(course_data)
                    return JsonResponse(data={"message": "Course Successfully Inserted"}, status=HTTP_201_CREATED)
                except:
                    return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            elif request.method == "PATCH":
                try:
                    database["course"].find_one_and_update(
                        filter={"_id": id}, update={"$set": data})
                    return JsonResponse(data={"message": "Course Successfully Updated"}, status=HTTP_200_OK)
                except:
                    return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "No Data Provided"}, status=HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={"message": "User Not Authorized"}, status=HTTP_400_BAD_REQUEST)

# Add this to views.py
@api_view(["GET"])
def list_students(request):
    """
    List all users with role 'Student' and return their id, first name, and last name
    """
    print("FETCHING STUDENTS")
    
    # Verify the token and get user info
    try:
        user = database[auth_collection].find_one(
            filter={"_id": request.id, "role": request.role})
        # role = user.get(role)
        print(request.role)
        # Authorization check - allow admin access
        if request.role.lower() == "college-admin" and user["_id"] == request.id:
            try:
                # Query all users with the Student role
                students = list(database[auth_collection].find(
                    {"role": "Student"}, 
                    {"_id": 1, "first_name": 1, "last_name": 1}
                ))
                
                # Convert ObjectId to string for JSON serialization
                for student in students:
                    student["_id"] = str(student["_id"])
                
                return JsonResponse(data={"students": students}, status=HTTP_200_OK)
            except Exception as e:
                return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "User Not Authorized"}, status=HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return JsonResponse(data={"message": "Invalid Token"}, status=HTTP_401_UNAUTHORIZED)


@api_view(["POST", "PATCH", "GET", "DELETE"])
def manage_subject(request, id=None):
    user = database[auth_collection].find_one(
        filter={"_id": request.id, "role": request.role})
    if user["role"] == "admin" and user["_id"] == request.id:
        data = request.data if request.data else {}

        if request.method == "DELETE":
            try:
                database["subject"].find_one_and_update(
                    filter={"_id": id}, update={"$set": {"is_deleted": True}})
                return JsonResponse(data={"message": "Record Successfully Deleted"}, status=HTTP_200_OK)
            except:
                return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == "GET":
            pipeline = [
                {
                    "$lookup": {
                        "from": "course",
                        "localField": "course_id",
                        "foreignField": "_id",
                        "as": "course"
                    }
                },
                {
                    "$lookup": {
                        "from": "semester",
                        "localField": "semester_id",
                        "foreignField": "_id",
                        "as": "semester"
                    }
                },
                {
                    "$unwind": "$course"
                },
                {
                    "$unwind": "$semester"
                },
                {
                    "$project": {
                        "subject_name": 1,
                        "course.course_name": 1,
                        "semester.semester_name": 1
                    }
                }
            ]
            try:
                subjects = database["subject"].aggregate(pipeline=pipeline)
                return JsonResponse(data={"subjects": subjects}, status=HTTP_200_OK)
            except:
                return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        if data:
            for field in data.keys():
                if field not in ("course_id", "semester_id", "subject_name", "subject_type"):
                    return JsonResponse(data={"message": "Wrong Data Provided"}, status=HTTP_400_BAD_REQUEST)

            if request.method == "POST":
                subject_data = {
                    "_id": create_unique_object_id(),
                    "course_id": data["course_id"],
                    "semester_id": data["semester_id"],
                    "subject_name": data["subject_name"],
                    "subject_type": data["subject_type"]
                }
                try:
                    database["subject"].insert_one(subject_data)
                    return JsonResponse(data={"message": "Subject Successfully Inserted"}, status=HTTP_201_CREATED)
                except:
                    return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            elif request.method == "PATCH":
                try:
                    database["subject"].find_one_and_update(
                        filter={"_id": id}, update={"$set": data})
                    return JsonResponse(data={"message": "Subject Successfully Updated"}, status=HTTP_200_OK)
                except:
                    return JsonResponse(data={"message": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(data={"message": "No Data Provided"}, status=HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={"message": "User not Authorized"}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def forgot_password(request, token=None):
    if request.method == "POST":
        email = request.POST["email"]
        user = database[auth_collection].find_one(
            {"email": email}, {"_id": 1, "role": 1, "email": 1})
        print(user)
        payload = {
            "id": user["_id"],
            "role": user["role"],
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=10)
        }
        token = jwt.encode(payload, jwt_secret, algorithm="HS256")
        if type(token) == str:
            token = base64.urlsafe_b64encode(
                token.encode("utf-8")).decode("utf-8")
            print(token)
            return JsonResponse([user, token], safe=False)
        return JsonResponse(user)

    elif request.method == "GET":
        if token:
            print(token)
            decoded_token = base64.b64decode(token).decode("utf-8")
            result = has_key(decoded_token)

            if type(result) == JsonResponse:
                return result

            if result is not None:
                print("has_key : ", result)
                # checking if expired
                if datetime.datetime.fromtimestamp(result['exp']) > datetime.datetime.now():
                    return JsonResponse("You can now reset your password.", safe=False)
            else:
                return JsonResponse(data={"message": "Token Expired!\nLogin Again"}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(decoded_token, safe=False)
        else:
            return JsonResponse(data={"message": "Token Not Provided"}, status=HTTP_400_BAD_REQUEST)


def has_key(token: str):
    try:
        return jwt.decode(token, jwt_secret, algorithms="HS256")
    except jwt.exceptions.ExpiredSignatureError as exp_err:
        return None
    except Exception:
        return JsonResponse(data={"message": "Token Corrupted!"}, status=status.HTTP_400_BAD_REQUEST)