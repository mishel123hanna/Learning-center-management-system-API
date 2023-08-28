from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from djoser.serializers import UserCreateSerializer


class ContactSerializer(serializers.ModelSerializer):
    class Meta():
        model = Contact
        fields = ['id', 'first_name', 'last_name',
                  'email', 'mobile', 'message']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta():
        model = Teacher
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    class Meta():
        model = Course
        fields = '__all__'
class CourseRetrieveSerializer(serializers.ModelSerializer):
    class Meta():
        model = Course
        fields = '__all__'
class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    class Meta():
        model = CustomUser
        fields = '__all__'


class NewCourseSerializer(serializers.ModelSerializer):
    class Meta():
        model = Course
        fields = '__all__'


class NewStudentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Student
        fields = '__all__'


class AdvertismentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Advertisement
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     # password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password',
#                   'phone_number', 'gender', 'birhdate']

#     # def create(self, validated_data):
#     #     user = User.objects.create_user(**validated_data)
#     #     return user

# User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'email')

# Register Serializer


# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'email', 'password',
#                   'birthdate', 'phone_number', 'gender')
#         extra_kwargs = {'password': {'write_only': True}}

# Register serializer
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta():
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password',
                  'phone_number', 'gender', 'birthdate')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


# CustomUser Profile

class CustomUserProfileSerializer(serializers.ModelSerializer):
    class Meta():
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'phone_number', 'gender', 'birthdate')


# Login Serializer

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

 # Student Serializer


class StudentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Student
        fields = '__all__'


# Marks

class MarkDetailsSerializer(serializers.ModelSerializer):
    class Meta():
        model = Mark
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
