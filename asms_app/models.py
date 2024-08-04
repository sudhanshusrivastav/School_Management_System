from django.db import models
from django.utils import timezone
# Create your models here.

class AcedemiaAdmin(models.Model):
    admin = models.BooleanField(default=True)
    utype = models.CharField(max_length=20,default='Admin')
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=32)
    pic = models.FileField(max_length=100, upload_to='Admin/')



class Student(models.Model):
    student = models.BooleanField(default=True)
    utype = models.CharField(max_length=20,default='Student')
    username = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=50)
    sfee = models.IntegerField()
    balance = models.IntegerField(default=0)
    sclass = models.CharField(max_length=50)
    fathers_name = models.CharField(max_length=50)
    DoB = models.DateField()
    fathers_phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=14)
    password = models.CharField(max_length=32, default="Student")
    address = models.TextField()
    pic = models.FileField(max_length=100, upload_to='Student/')
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.name



class Teacher(models.Model):
    teacher = models.BooleanField(default=True)
    utype = models.CharField(max_length=20,default='Teacher')
    username = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    tclass = models.CharField(max_length=50)
    pic = models.FileField(max_length=100, upload_to='Teacher/' , default="")
    password = models.CharField(max_length=32, default="Teaceher")
    phone = models.CharField(max_length=14)
    tsalary = models.CharField(max_length=50)
    address = models.TextField()
    qualification = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.name



class LoginUser(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=32)
    usertype = models.CharField(max_length=20)



class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    paid = models.IntegerField()
    date = models.DateField(default=timezone.now)
    due = models.CharField(max_length=20, default=None)
    payment = models.FileField(max_length=100, upload_to='Payments/')
    status = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['date','-updated','-created']



class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now) 

    class Meta:
        ordering = ['date', 'student'] 

    def __str__(self):
        return f"{self.student.name} - {self.date.strftime('%Y-%m-%d')}"
    


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    class Meta:
        ordering = ['date','teacher']

    def __str__(self):
        return f"{self.teacher.name} - {self.date.strftime('%Y-%m-%d')}"


class Class(models.Model):
    name = models.CharField(max_length=50)
    seats = models.IntegerField(default=60)
    roomno = models.CharField(max_length=5)



class Salary(models.Model):
    date = models.DateField(auto_now=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    paid = models.IntegerField()
    due = models.CharField(max_length=20, default="None", null=True)
    status = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['date','-updated','-created']



class Fund(models.Model):
    amount = models.IntegerField(default=100000)
    debit = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    


class Subjects(models.Model):
    name = models.CharField(max_length=20)
    subclass = models.CharField(max_length=3)



class Query(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    question = models.TextField()
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated','-created']


class Reply(models.Model):
    query = models.ForeignKey(Query, on_delete=models.DO_NOTHING)
    repliedby = models.CharField(max_length=30)
    reply = models.TextField()
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated','-created']


class Exam(models.Model):
    ofclass = models.CharField(max_length=10)
    examname = models.CharField(max_length=20)
    examdate = models.DateField(default=timezone.now)
    examtime = models.TimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-examdate','-created']



class Homework(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    homework = models.CharField(max_length=100)
    desc = models.TextField(default='Regular Homework')
    submit_till = models.DateField(default=timezone.now)
    class Meta:
        ordering = ['submit_till']