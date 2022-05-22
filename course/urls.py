from django.urls import path
from .views import CourseViews, CourseIDViews, create_instructor, create_students

urlpatterns = [
    path('courses/', CourseViews.as_view()),
    path('courses/<course_id>/', CourseIDViews.as_view()),
    path('courses/<course_id>/registrations/instructor/', create_instructor),
    path('courses/<course_id>/registrations/students/', create_students),	
]