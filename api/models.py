
from django.db import models
from django.utils import timezone
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, Group, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.contrib.auth.models import Permission
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
# Create your models here.


class Teacher(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    picture_teacher = models.ImageField(null=True)
    details = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL = (
        ('بكالوريا', "بكالوريا"), ("تاسع", "تاسع")
    )
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, db_index=True)
    max_students = models.PositiveIntegerField(default=20)
    number_of_students = models.PositiveIntegerField(default = 0)
    picture_course= models.URLField(default ="null" )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,  null=True, blank=True, db_index=True)
    session_num = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    details = models.TextField(max_length=1000)
    state = models.BooleanField(default=True)
    level = models.CharField(
        max_length=50, choices=LEVEL)
    course_teacher = models.ManyToManyField(Teacher, through='CourseTeacher')

    def __str__(self):
        return self.name + "(" + self.level + ")"


class CourseTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    session_num = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        self.name = f"{self.teacher.name} - {self.course.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    custom_user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True)
    birthdate = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    objects = CustomUserManager()

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if not created:
          # update the existing token if the user is being updated
            try:
                token = Token.objects.get(user=self)
                token.delete()
            except Token.DoesNotExist:
                pass

        # create or update the token associated with the student object
        try:
            student = Student.objects.get(user=self)
            token = Token.objects.create(user=self)
            student.token = token.key
            student.save()
        except Student.DoesNotExist:
            # handle the case where the student does not exist
            pass


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, db_index=True)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, db_index=True)
    email = models.EmailField(null=True)
    student_number = models.IntegerField()
    father_number = models.IntegerField()
    mother_number = models.IntegerField()
    address = models.CharField(max_length=50)
    father_work = models.CharField(max_length=50)
    mother_work = models.CharField(max_length=50)
    student_course = models.ManyToManyField(
        Course, through='StudentCourse', related_name='students')

    def __str__(self):
        return self.first_name


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # absence_num = models.IntegerField()
    
    def __str__(self):
        return self.student.first_name + ": " + self.course.name


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    class_name = models.CharField(max_length=50)
    teacher_category = models.ManyToManyField(
        Teacher, through="TeacherCategory")

    def __str__(self):
        return self.name


class TeacherCategory(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)


class Mark(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.PROTECT)
    mark = models.FileField(null=True, blank=True)


class Advertisement(models.Model):
    date = models.DateField()
    image = models.ImageField(upload_to='media')


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        send_mail(
            'Contact Query',  # subject
            'here is the message',  # message
            'mishelhanna3@gmail.com',  # email
            [self.email],  # toemail
            fail_silently=False,
            html_message=f'<p>{self.first_name}</p><p>{self.message}</p>',
            # recipient_list=

        )
        return super(Contact, self).save(*args, **kwargs)

    class Meta():
        verbose_name_plural = "Contact Queries"


@receiver(post_save, sender=CustomUser)
def link_student(sender, instance, created, **kwargs):
    if created:
        try:
            student = Student.objects.get(student_number=instance.phone_number)
            student.user = instance
            student.save()
        except Student.DoesNotExist:
            pass
