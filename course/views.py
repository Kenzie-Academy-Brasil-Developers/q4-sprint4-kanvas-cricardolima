from re import U
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from django.db import IntegrityError

from course.models import Courses
from course.serializers import CourseSerializer, CourseUUIDSerializer, CreateStudentSerializer, UpdateCourseSerializer, CreateInstructorSerializer
from course.permissions import UserAuthenticated
from user.models import User

class CourseViews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserAuthenticated]
    
    def post(self, request: Request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        course_found = Courses.objects.filter(name=serializer.validated_data['name']).exists()
        
        if course_found:
            return Response({"message": "Course already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        course = Courses.objects.create(**serializer.validated_data)
        course.save()
        
        serializer = CourseSerializer(course)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request: Request):
        courses = Courses.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CourseIDViews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserAuthenticated]
    
    def get(self, _: Request, course_id: int):
        course = Courses.objects.filter(uuid=course_id).first()
        serializer = CourseSerializer(course)
        
        if not course: 
            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
       
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request: Request, course_id: int):
        serializer = UpdateCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            course_found = Courses.objects.filter(uuid=course_id)
            course_found.update(**serializer.validated_data)
            course = Courses.objects.filter(uuid=course_id).first()
            course_updated = CourseSerializer(course)
            
            if not course_found:
                return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            return Response(course_updated.data, status=status.HTTP_200_OK)
        
        except IntegrityError:
            return Response({"message": "This course name already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def delete(self, _: Request, course_id: int):
        course = Courses.objects.filter(uuid=course_id).first()
        
        if not course:
            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        course.delete()
        
        return Response("", status=status.HTTP_204_NO_CONTENT)
    
@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([UserAuthenticated])
def create_instructor(request: Request, course_id):
    instructor_serializer = CreateInstructorSerializer(data=request.data)
    instructor_serializer.is_valid(raise_exception=True)

    try:
        instructor = User.objects.get(uuid=instructor_serializer.validated_data['instructor_id'])
    except User.DoesNotExist:
        return Response(
            {"message": 'Invalid instructor_id'}, status.HTTP_404_NOT_FOUND
        )

    if not instructor.is_admin:
        return Response({"message": "Instructor id does not belong to an admin"}, status.HTTP_422_UNPROCESSABLE_ENTITY)


    course_serializer = CourseUUIDSerializer(data={"course_id": course_id})
    if not course_serializer.is_valid():
        return Response(
            {"message": "Course does not exist"}, status.HTTP_404_NOT_FOUND
        )

    course = Courses.objects.filter(uuid = course_serializer.validated_data["course_id"]).first()
    
    if not course:
        return Response({"message": "Course does not exist"}, status.HTTP_404_NOT_FOUND)

    instructor_already_registered = Courses.objects.filter(instructor= instructor.uuid).first()

    if instructor_already_registered:
        instructor_already_registered.instructor = None
        instructor_already_registered.save()

    course.instructor = instructor
    course.save()

    try:
        course = Courses.objects.get(uuid=course_serializer.validated_data['course_id'])
    except Courses.DoesNotExist:
        return Response(
            {"message": "Course does not exist"}, status.HTTP_404_NOT_FOUND
        )
    course = CourseSerializer(course)

    return Response(course.data, status.HTTP_200_OK)
    
@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([UserAuthenticated])
def create_students(request: Request, course_id: str):
    serializer = CreateStudentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        course_to_update = Courses.objects.filter(pk=course_id).first()
        students = [
            User.objects.filter(pk=student_uuid).first()
            for student_uuid
            in serializer.validated_data["students_id"]
        ]

        if not course_to_update:
            return Response(
                {"message": "Course does not exist"},
                status.HTTP_404_NOT_FOUND
            )

        if None in students:
            return Response(
                {"message": "Invalid students_id list"},
                status.HTTP_404_NOT_FOUND
            )

        if True in [item.is_admin for item in students]:
            return Response(
                {"message": "Some student id belongs to an Instructor"},
                status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        course_to_update.students.set(serializer.validated_data["students_id"])
        course = Courses.objects.filter(pk=course_id).first()
        course_updated = CourseSerializer(course)
        course_updated = course_updated.data

        return Response(
            course_updated,
            status.HTTP_200_OK
        )

    except ValidationError as e:

        return Response(
            {"message": "Course does not exist"},
            status.HTTP_404_NOT_FOUND
        )