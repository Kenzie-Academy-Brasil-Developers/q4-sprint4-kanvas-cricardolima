from rest_framework import serializers

from user.serializers import UsersSerializer

class CourseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    demo_time = serializers.TimeField()
    created_at = serializers.DateField(read_only=True)
    link_repo = serializers.CharField()
    instructor = UsersSerializer(required=False)
    students = UsersSerializer(many=True, required=False)
    
    
class UpdateCourseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=False)
    demo_time = serializers.TimeField(required=False)
    link_repo = serializers.CharField(required=False)
    
class CreateInstructorSerializer(serializers.Serializer):
    instructor_id = serializers.CharField()
    
class CreateStudentSerializer(serializers.Serializer):
    students_id = serializers.ListField(child=serializers.CharField())
    
class CourseUUIDSerializer(serializers.Serializer):
    course_id = serializers.UUIDField()