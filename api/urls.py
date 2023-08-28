from django.urls import path, include

from . import views
from .views import *

app_name = 'api'

urlpatterns = [
    # add teacher
    path('new-teacher/', NewTeacherAPIView.as_view()),
    # add course
    path('new-course/', NewCourseAPIView.as_view()),
    # add student
    path('new-student/', NewStudentAPIView.as_view()),
    # ///////////////////////////////////////////


    path('contact/', ContactListAPIView.as_view()),

    # display students
    path('students/', StudentsAPIView.as_view()),
    # display Student by id
    path('students/<int:id>', OneStudentAPIView.as_view()),
    # api for display teachers
    path('teachers/', TeachersAPIView.as_view()),
    # display teacher by id
    path('teachers/<int:id>', OneTeacherAPIView.as_view()),

    # api for display courses
    path('courses/', CourseListAPIView.as_view()),
    # details for one course
    path('courses/<int:course_id>', CourseRetreiveAPIView.as_view()),
    # display course's teacher
    path('courses/<int:course_id>/teachers/',
         CourseTeacherView.as_view(), name='course-teachers'),

    # Register
    path('register/', RegisterView.as_view(), name='register'),
    # Login
    path('login/', LoginView.as_view(), name='login'),
    # Logout
    path('logout/', LogoutView.as_view(), name='logout'),
    # Edit Profile
    path('edit-info/', UserProfileUpdateView.as_view()),
    # change password
    path('change-password/', ChangePasswordView.as_view()),
    # display advertisment
    path('advertisments/<int:adver_id>', views.get_advertisment),
    # display all advertisments
    path('advertisments/', AdvertismentList.as_view()),
    # Student Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    # Enroll Course
    path('enroll-course/', EnrollStudentView.as_view()),
    # Delete Enrolled Course
    path('delete-enrolled-course/', DeleteEnrolledCourseView.as_view()),
    # Enrolled Courses
    path('enrolled-courses/', EnrolledCoursesView.as_view(), name='enrolled-classe'),
    # users
    path('custom-users/', CustomUserView.as_view()),
    path('custom-users/<int:custom_user_id>', OneCustomUserAPIView.as_view()),
    # Marks
    path('marks/', MarkDetailsView.as_view()),
    # Search Students
    path('search/students/', StudentSearchView.as_view(), name='student_search'),
    # Search Courses
    # path('search/courses/', CourseSearchView.as_view()),
    path('search/courses/', CourseSearchByClassView.as_view()),
    # course's marks
    path('course/<int:course_id>/marks/', CourseMarkAPIView.as_view())
]
