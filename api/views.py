from djoser.views import TokenCreateView
from djoser.views import UserViewSet
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login as django_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.

def home(request):
    return HttpResponse("<h1 style ='text-align:center'>Welcom</h1>")
class ContactListAPIView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class NewTeacherAPIView(generics.CreateAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class TeachersAPIView(generics.ListAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class OneTeacherAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    lookup_field = 'id'


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()


class CourseRetreiveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseRetrieveSerializer
    queryset = Course.objects.all()
    lookup_field = 'course_id'


class NewCourseAPIView(generics.CreateAPIView):
    serializer_class = NewCourseSerializer
    queryset = Course.objects.all()


class NewStudentAPIView(generics.CreateAPIView):
    serializer_class = NewStudentSerializer
    queryset = Student.objects.all()


class StudentsAPIView(generics.ListAPIView):
    serializer_class = NewStudentSerializer
    queryset = Student.objects.all()


class OneStudentAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewStudentSerializer
    queryset = Student.objects.all()
    lookup_field = 'id'

class OneCustomUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserRetrieveSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'custom_user_id'

def get_advertisment(request, adver_id):
   # Retrieve the Advertisment object from the database using the adver_id
    adver = get_object_or_404(Advertisement, id=adver_id)

    # Open the image file and return it as a FileResponse
    return FileResponse(adver.image, as_attachment=True)


class AdvertismentList(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertismentSerializer


# display course's teacher

class CourseTeacherView(APIView):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        teachers = course.course_teacher.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)


# Enroll course

class EnrollStudentView(APIView):
    # Add authentication class
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Add permission class

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            student = user.student
            student_id = student.student_id
            # student_id = request.data.get('student_id')
            course_id = request.data.get('course_id')

            # print(student_id)
            # print(request.data)

            student = get_object_or_404(Student, pk=student_id)

            course = get_object_or_404(Course, pk=course_id)
            if course.students.filter(pk=student_id).exists():
                return JsonResponse({'message': 'Student already enrolled in this course'})
            if course.number_of_students >= course.max_students:
                return JsonResponse({'message': 'Course is full'})
            enrollment = StudentCourse(student=student, course=course)
            enrollment.save()
            course.number_of_students += 1
            course.save()

            return JsonResponse({'message': 'Student enrolled in course successfully'})
        except:
            return JsonResponse({"message": "user didn't a student in our system"})


class DeleteEnrolledCourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            student = user.student
            student_id = student.student_id
            course_id = request.data.get('course_id')

            student = get_object_or_404(Student, pk=student_id)
            course = get_object_or_404(Course, pk=course_id)

            # Check if the student is enrolled in the course
            enrollment = StudentCourse.objects.filter(
                student=student, course=course).first()
            if not enrollment:
                return JsonResponse({'message': 'Student is not enrolled in this course'})

            # Delete the enrollment and update course information
            enrollment.delete()
            course.number_of_students -= 1
            course.save()

            return JsonResponse({'message': 'Enrollment deleted successfully'})
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return JsonResponse({"message": "An error occurred while processing the request"})


# Enrolled Courses


class EnrolledCoursesView(generics.ListAPIView):

    serializer_class = CourseListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            student = self.request.user.student

            enrolled_courses = student.student_course.all()

            return enrolled_courses
        except Student.DoesNotExist:
            return Course.objects.none()


# Register Custom User
class RegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)


# Login Custom User

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


# Logout

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            token = request.auth
            token.delete()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Successfully logged out.'}, status=status.HTTP_200_OK)


# Student Profile

class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # print(request.user)
        user = request.user
        serializer = CustomUserProfileSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Edit Profile

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = CustomUserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)

        if serializer.is_valid():
            user = request.user

            serializer.update(user, serializer.validated_data)
            # update the token after user object has been saved
            try:
                token = Token.objects.get(user=user)
                token.save()
            except Token.DoesNotExist:
                new_token = Token.objects.create(user=user)

            return Response({"detail": "Profile updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Change Password

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            # check if old password is correct
            if not request.user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # change password and update session auth hash
            request.user.password = make_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Customer Users
class CustomUserView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


# Marks

class MarkDetailsView(generics.ListAPIView):
    serializer_class = MarkDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            student = self.request.user.student
            if student:
                # only students can see mark file
                return Mark.objects.all()
        except:
            return Response({'error': 'you are not student'}, status=status.HTTP_400_BAD_REQUEST)


# Search about Students

class StudentSearchView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        students = Student.objects.filter(
            Q(first_name__icontains=query) |
            Q(phone_number__icontains=query)
        )
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Search Courses

# class CourseSearchView(APIView):
#     def get(self, request):
#         query = request.GET.get('query')
#         courses = Course.objects.filter(
#             Q(name__icontains=query) |
#             Q(level__icontains=query)
#         )
#         serializer = CourseListSerializer(courses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# تاسع او بكالوريا


class CourseSearchByClassView(APIView):
    def get(self, request):
        level = request.GET.get('level')
        courses = Course.objects.filter(level=level)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# course's Marks


class CourseMarkAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        marks = Mark.objects.filter(course_id=course_id)
        serializer = MarkDetailsSerializer(marks, many=True)
        return Response(serializer.data)
