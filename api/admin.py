from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


admin.site.register([Contact, Student, StudentCourse, Mark, Teacher,
                    Category, TeacherCategory, Course, CourseTeacher, Advertisement, CustomUser])
