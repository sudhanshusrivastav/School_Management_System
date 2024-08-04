# forms.py
from django import forms
from .models import Student, Teacher, AcedemiaAdmin, Query, Reply

class EditStudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phone', 'email', 'password', 'pic']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password


class EditTeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['email', 'phone', 'password', 'pic']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
    


class EditAdminProfileForm(forms.ModelForm):
    class Meta:
        model = AcedemiaAdmin
        fields = ['name', 'username', 'password', 'pic']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
        

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control'}),
        }
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'class': 'form-control'}),
        }