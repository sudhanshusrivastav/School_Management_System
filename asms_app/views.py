from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from itertools import chain
from operator import attrgetter
from datetime import datetime, timedelta
from .forms import EditStudentProfileForm, EditTeacherProfileForm, EditAdminProfileForm,QueryForm, ReplyForm
from django.views.generic import ListView
# Create your views here.
def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            obj = LoginUser.objects.get(username=username, password=password)
            if obj:
                request.session['session_key'] = username
                return redirect('dashboard')
        except:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def dashboard(request):
    fund = Fund.objects.first()
    notice = Exam.objects.all()
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    recent_credits = Fee.objects.order_by('-date')[:3]  
    recent_debits = Salary.objects.order_by('-date')[:3]
    new_students = Student.objects.order_by('-created')[:5]  
    new_teachers = Teacher.objects.order_by('-created')[:5]
    key = request.session.get('session_key')
    combined_transactions = sorted(
        chain(recent_credits, recent_debits),
        key=attrgetter('date'),
        reverse=True
    )
    last_three_transactions = combined_transactions[:3]
    
    user = None
    studentss = None
    homework_list = None
    teacherss = None
    queries = None
    salariess = None
    if key:
        obj = LoginUser.objects.get(username=key)
        if obj.usertype == 'admin':
            user = AcedemiaAdmin.objects.get(username=key)
        elif obj.usertype == 'student':
            user = Student.objects.get(username=key)
            homework_list = Homework.objects.filter(student=user)
            queries = Query.objects.filter(student=user)
            teacherss = Teacher.objects.filter(tclass=user.sclass)
        elif obj.usertype == 'teacher':
            user= Teacher.objects.get(username=key)
            studentss = Student.objects.filter(sclass=user.tclass)
            salariess = Salary.objects.filter(teacher=user)[:3]
        context = {
                    'user':user, 
                    'last_three_transactions': last_three_transactions,
                    'studentss':studentss,
                    'teacherss':teacherss,
                    'queries':queries,
                    'total_teachers': total_teachers,
                    'total_students': total_students,
                    'fund':fund,
                    'notices':notice,
                    'recent_debits': recent_debits, 
                    'recent_credits': recent_credits,
                    'students':new_students,
                    'teachers':new_teachers,
                    'homework_list':homework_list,
                    'salariess':salariess,
                   }
        return render(request, 'home.html', context)
    else:
        return redirect('home')


def addstudent(request):
    key = request.session.get('session_key')
    class_values = range(1, 11) 
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
            if request.method == 'POST':
                username = request.POST['username']
                name = request.POST['name']
                sfee = request.POST['sfee']
                sclass = request.POST['sclass']
                fathers_name = request.POST['fathers_name']
                DoB = request.POST['DoB']
                fathers_phone = request.POST['fathers_phone']
                email = request.POST['email']
                phone = request.POST['phone']
                password = request.POST.get('password', 'Student')
                address = request.POST['address']
                pic = request.FILES.get('pic') 
                u = LoginUser.objects.filter(username=username)
                e = Student.objects.filter(email=email)
                p = Student.objects.filter(phone=phone)

                if e or p:
                    messages.error(request, 'Email Or Phone already Exist')
                    return redirect('addstudent')
                if u :
                    messages.error(request, 'Username Already Exist')
                    return redirect('addstudent')
                # Create the Student instance
                new_student = Student(
                    username=username,
                    name=name,
                    sfee=sfee,
                    sclass=sclass,
                    fathers_name=fathers_name,
                    DoB=DoB,
                    fathers_phone=fathers_phone,
                    email=email,
                    phone=phone,
                    password=password,
                    address=address,
                    pic=pic
                )
                loginobj = LoginUser(username=username, password=password, usertype='student')
                loginobj.save()
                messages.success(request, 'Student Added')
                new_student.save()
        except:
            return redirect('home')
    return render(request, 'addstudent.html', {'user':user, 'class':class_values})




def addteacher(request):
    key = request.session.get('session_key')
    class_values = range(1, 11) 
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
            if request.method == 'POST':
                username = request.POST['username']
                name = request.POST['name']
                email = request.POST['email']
                tclass = request.POST['tclass']
                password = request.POST.get('password', 'Teacher')
                phone = request.POST['phone']
                tsalary = request.POST['tsalary']
                address = request.POST['address']
                qualification = request.POST['qualification']
                experience = request.POST['experience']
                pic = request.FILES.get('pic') 
                u = LoginUser.objects.filter(username=username)
                e = Teacher.objects.filter(email=email)
                p = Teacher.objects.filter(phone=phone)
                t = Teacher.objects.filter(tclass=tclass)
                if u :
                    messages.error(request, 'Username Already Exist')
                    return redirect('addteacher')

                if e or p:
                    messages.error(request, 'Email Or Phone already Exist')
                    return redirect('addteacher')
                # Create the Teacher instance
                if t:
                    messages.error(request, f'Class Teacher of class {tclass} Already Assigned')
                    return redirect('addteacher')
                

                new_teacher = Teacher(
                    username=username,
                    name=name,
                    email=email,
                    tclass=tclass,
                    password=password,
                    phone=phone,
                    tsalary=tsalary,
                    address=address,
                    qualification=qualification,
                    experience=experience,
                    pic=pic
                )
                loginobj = LoginUser(username=username, password=password, usertype='teacher')
                loginobj.save()
                messages.success(request, 'Teacher Added')
                new_teacher.save()
                return redirect('dashboard')
        except AcedemiaAdmin.DoesNotExist:
            return redirect('home')
    return render(request, 'addteacher.html', {'user': user, 'class':class_values})



def mark_attendance(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Teacher.objects.get(username=key)
            if request.method == 'POST':
                date_str = request.POST.get('date')
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                
                StudentAttendance.objects.filter(date=date).delete()
                for student in Student.objects.all():
                    status = request.POST.get(f'attendance[{student.username}]')
                    if status is not None:
                        attendance = StudentAttendance(student=student, status=status, date=date)
                        attendance.save()
                
                return redirect('view_attendance')
        except Teacher.DoesNotExist:
            return redirect('home')

    selected_date = request.GET.get('date') or datetime.now().date()

    students = Student.objects.filter(sclass=user.tclass)

    return render(request, 'mark_attendance.html', {'user': user, 'students': students, 'selected_date': selected_date})


def mark_teacher_attendance(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
            if request.method == 'POST':
                date_str = request.POST.get('date')
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                
                TeacherAttendance.objects.filter(date=date).delete()

                for teacher in Teacher.objects.all():
                    status = request.POST.get(f'attendance[{teacher.username}]', 'False')  # Default status is False (Absent)
                    attendance_record = TeacherAttendance(teacher=teacher, status=status, date=date)
                    attendance_record.save()
                
                return redirect('view_teacher_attendance')
        except AcedemiaAdmin.DoesNotExist:
            return redirect('home')

    selected_date = request.GET.get('date') or timezone.now().date()

    teachers = Teacher.objects.all()

    return render(request, 'teacherattendance.html', {'user': user, 'teachers': teachers, 'selected_date': selected_date})



def view_attendance(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Teacher.objects.get(username=key)
        except Teacher.DoesNotExist:
            try:
                user = AcedemiaAdmin.objects.get(username=key)
            except AcedemiaAdmin.DoesNotExist:
                try:
                    user = Student.objects.get(username=key)
                except Student.DoesNotExist:
                    return redirect('home')
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        attendances = StudentAttendance.objects.filter(date=selected_date)
        return render(request, 'view_attendance.html', {'user': user, 'attendances': attendances, 'selected_date': selected_date})
    

    selected_date = datetime.now().date()
    attendances = StudentAttendance.objects.filter(date=selected_date)
    
    return render(request, 'view_attendance.html', {'user': user, 'attendances': attendances, 'selected_date': selected_date})



def view_teacher_attendance(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Teacher.objects.get(username=key)
        except Teacher.DoesNotExist:
            try:
                user = AcedemiaAdmin.objects.get(username=key)
            except AcedemiaAdmin.DoesNotExist:
                try:
                    user = Student.objects.get(username=key)
                except Student.DoesNotExist:
                    return redirect('home')

    if request.method == 'POST':
        selected_date = request.POST.get('date')
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        attendances = TeacherAttendance.objects.filter(date=selected_date)
        return render(request, 'view_teacher_attendance.html', {'user': user, 'attendances': attendances, 'selected_date': selected_date})

    

    selected_date = datetime.now().date()
    attendances = TeacherAttendance.objects.filter(date=selected_date)
    
    return render(request, 'view_teacher_attendance.html', {'user': user, 'attendances': attendances, 'selected_date': selected_date})



def view_students(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Teacher.objects.get(username=key)
        except Teacher.DoesNotExist:
            try:
                user = AcedemiaAdmin.objects.get(username=key)
            except AcedemiaAdmin.DoesNotExist:
                try:
                    user = Student.objects.get(username=key)
                except Student.DoesNotExist:
                    return redirect('home')
    students = Student.objects.all()
    return render(request, 'viewstudents.html', {'user':user,'students': students})



def view_teachers(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Teacher.objects.get(username=key)
        except Teacher.DoesNotExist:
            try:
                user = AcedemiaAdmin.objects.get(username=key)
            except AcedemiaAdmin.DoesNotExist:
                try:
                    user = Student.objects.get(username=key)
                except Student.DoesNotExist:
                    return redirect('home')
    teacher = Teacher.objects.all()
    return render(request, 'viewteachers.html', {'user':user,'teachers': teacher})


def remove_student(request, username):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
            if request.method == 'POST':
                student = Student.objects.get(username=username)
                student.delete()
                return redirect('view_students')
        except:
            return redirect('home')
    return redirect('view_students')



def remove_teacher(request, username):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
            if request.method == 'POST':
                teacher = Teacher.objects.get(username=username)
                teacher.delete()
                return redirect('view_teachers')
        except:
            return redirect('home')
    return redirect('view_teachers')



def edit_student_profile(request):
    try:
        student = Student.objects.get(username=request.session.get('session_key'))
    except:
        return redirect('home')
    
    if request.method == 'POST':
        form = EditStudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to a profile view after saving
    else:
        form = EditStudentProfileForm(instance=student)
    
    return render(request, 'edit_student_profile.html', {'user':student,'form': form})



def edit_teacher_profile(request):
    
    try:
        teacher = Teacher.objects.get(username=request.session.get('session_key'))
    except:
        return redirect('home')
    
    if request.method == 'POST':
        form = EditTeacherProfileForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to a profile view after saving
    else:
        form = EditTeacherProfileForm(instance=teacher)
    
    return render(request, 'edit_teacher_profile.html', {'user':teacher,'form': form})


def edit_admin_profile(request):
    try:
        teacher = admin = AcedemiaAdmin.objects.get(username=request.session.get('session_key'))
    except:
        return redirect('home')
    
    if request.method == 'POST':
        form = EditAdminProfileForm(request.POST, request.FILES, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = EditAdminProfileForm(instance=admin)
    
    return render(request, 'edit_admin_profile.html', {'user':admin,'form': form})



def view_class_students(request):
    try:
        teacher = Teacher.objects.get(username=request.session.get('session_key'))
    except:
        return redirect('home')
    teacher_class = teacher.tclass  
    
    students = Student.objects.filter(sclass=teacher_class)

    return render(request, 'view_class_students.html', {'user':teacher,'students': students})





def assign_homework(request, username):
    teacher = None
    key = request.session.get('session_key')
    if key:
        teacher = get_object_or_404(Teacher, username=key)
        student = get_object_or_404(Student, username=username)
    
    if teacher: 
        if request.method == 'POST':
            homework = request.POST.get('homework')
            desc = request.POST.get('desc')
            submit_till = request.POST.get('submit_till')
            
            Homework.objects.create(teacher=teacher, student=student, homework=homework, desc=desc, submit_till=submit_till)
            
            messages.success(request, f'Homework Assigned to {student.name}')
            return redirect('view_class_students')
        else:
            return render(request, 'assign_homework.html', {'user':teacher,'student': student})
    else:
        return redirect('home')  
    


def view_homework(request):
    key = request.session.get('session_key')
    if key: 
        student = get_object_or_404(Student, username=key)
        homework_list = Homework.objects.filter(student=student)
        return render(request, 'view_homework.html', {'user':student,'homework_list': homework_list})
    else:
        return redirect('home') 
    


def add_exam(request):
    key = request.session.get('session_key')
    user = None
    notices = Exam.objects.all()
    if key:
        try:
            user = Teacher.objects.get(username=key)
        except Teacher.DoesNotExist:
            try:
                user = AcedemiaAdmin.objects.get(username=key)
            except AcedemiaAdmin.DoesNotExist:
                return redirect('home')
    if request.method == 'POST':
        ofclass = request.POST.get('ofclass')
        examname = request.POST.get('examname')
        examdate = request.POST.get('examdate')
        examtime = request.POST.get('examtime')

        exam = Exam(ofclass=ofclass, examname=examname, examdate=examdate, examtime=examtime)
        exam.save()
        messages.success(request, 'Notice added successfully.')
        
        return redirect('notice')

    return render(request, 'notice.html', {'user':user, 'notices':notices})


def view_notice(request):
    try:
        student = Student.objects.get(username=request.session.get('session_key'))
    except:
        return redirect('home')
    student_class = student.sclass 

    notices = Exam.objects.filter(ofclass=student_class)

    return render(request, 'view_notice.html', {'user':student,'notices': notices})


def all_queries(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Teacher.objects.get(username=key)
        except Teacher.DoesNotExist:
            try:
                user = AcedemiaAdmin.objects.get(username=key)
            except AcedemiaAdmin.DoesNotExist:
                try:
                    user = Student.objects.get(username=key)
                except Student.DoesNotExist:
                    return redirect('home')
            
    queries = Query.objects.all()
    return render(request, 'queries.html', {'user':user, 'queries':queries})


def post_query(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Student.objects.get(username=key)
        except Student.DoesNotExist:
            return redirect('home')
    queries = Query.objects.filter(student=user)
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.student = user  
            query.save()
            messages.success(request, 'Query Added')
            return redirect('post_query')
    else:
        form = QueryForm()
    return render(request, 'post_query.html', {'user':user,'form': form, 'queries':queries})

def query_detail(request, query_id):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Teacher.objects.get(username=key)
        except Teacher.DoesNotExist:
            try:
                user = AcedemiaAdmin.objects.get(username=key)
            except AcedemiaAdmin.DoesNotExist:
                try:
                    user = Student.objects.get(username=key)
                except Student.DoesNotExist:
                    return redirect('home')
    query = Query.objects.get(pk=query_id)
    replies = Reply.objects.filter(query=query)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.query = query
            reply.repliedby = user.utype +": "+ user.name 
            reply.save()
            return redirect('query_detail', query_id=query_id)
    else:
        form = ReplyForm()
    return render(request, 'post_reply.html', {'user':user,'query': query, 'replies': replies, 'form': form})


def subjects(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Teacher.objects.get(username=key)
            subclass = user.tclass
        except Teacher.DoesNotExist:
                try:
                    user = Student.objects.get(username=key)
                    subclass = user.sclass
                except Student.DoesNotExist:
                    return redirect('home')
    subjects = Subjects.objects.filter(subclass=subclass)
    return render(request, 'subjects.html', {'user':user,'subjects': subjects})


def add_subject(request):
    try:
        user = AcedemiaAdmin.objects.get(username=request.session.get('session_key'))
    except AcedemiaAdmin.DoesNotExist:
        return redirect('home')
    subjects = Subjects.objects.all()
    subclass_values = range(1, 11) 
    subjects_list = [
        'Mathematics',
        'English Language',
        'Physics',
        'Chemistry',
        'Biology',
        'History',
        'Geography',
        'Physical Education',
        'Foreign Languages',
        'Computer Science',
        'Art (Visual Arts)',
        'Music'
    ]
    if request.method == 'POST':
        name = request.POST['name']
        subclass = request.POST['subclass']
        x = Subjects.objects.filter(name=name)
        if x:
            messages.error(request, 'Can Not Add Duplicate Subjects')
            return redirect('addsubjects')
        obj = Subjects()
        obj.subclass = subclass
        obj.name = name
        obj.save()
        messages.success(request, 'Subject Added')
        return redirect('addsubjects')
    else:
        return render(request, 'add_subjects.html', {'user':user, 'subjects':subjects,'subclass_values': subclass_values,'subjects_list': subjects_list})




def funds(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
        except AcedemiaAdmin.DoesNotExist:
            return redirect('home')
    fund = Fund.objects.first()

    recent_debits = Salary.objects.order_by('-date')[:5]  
    total_debit = sum(salary.amount for salary in recent_debits)

    recent_credits = Fee.objects.order_by('-date')[:5]  
    total_credit = sum(fee.paid for fee in recent_credits)
    

    # Get previous total debits and credits from session or default to 0
    previous_debit = request.session.get('previous_debit', 0)
    previous_credit = request.session.get('previous_credit', 0)

    # Calculate the difference between current and previous totals
    debit_diff = total_debit - previous_debit
    credit_diff = total_credit - previous_credit

    # Update fund with the difference
    fund.debit += debit_diff
    fund.credit += credit_diff
    fund.amount += credit_diff - debit_diff
    fund.save()

    # Update session with current totals for next iteration
    request.session['previous_debit'] = total_debit
    request.session['previous_credit'] = total_credit

    return render(request, 'funds.html', {'user':user,'fund': fund, 'recent_debits': recent_debits, 'recent_credits': recent_credits})


def salary(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
        except AcedemiaAdmin.DoesNotExist:
            return redirect('home')
    teacher = Teacher.objects.all()
    paidsalary = Salary.objects.all()
    return render(request, 'salary.html', {'user':user,'teachers': teacher, 'salary':paidsalary})



def pay_salary(request, username):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
        except AcedemiaAdmin.DoesNotExist:
            return redirect('home')
    teacher = Teacher.objects.get(username=username)
    
    recent_payment = Salary.objects.filter(teacher=teacher, date__gte=timezone.now() - timezone.timedelta(days=30)).exists()
    if recent_payment:
        messages.error(request, f"{teacher.name} has already received a salary payment recently. Cannot pay again.")
        return redirect('salary')  
    
    if request.method == 'POST':
        paid = int(request.POST.get('paid')) if request.POST.get('paid') else 0  
        amount = teacher.tsalary if teacher.tsalary else 0  
        due = int(amount) - int(paid) if amount and paid else int(amount) 
        
        salary = Salary.objects.create(
            teacher=teacher,
            amount=amount,
            paid=paid,
            due=due,
            status=True
        )
        messages.success(request, f'Salary {paid} Paid to {teacher.name} Due is {due}')
        return redirect('salary')  

    return render(request, 'pay_salary.html', { 'user':user,'teacher': teacher})



def view_salary(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Teacher.objects.get(username=key)
        except Teacher.DoesNotExist:
            return redirect('home')
        
    sobj = Salary.objects.filter(teacher=user)
    return render(request, 'view_salary.html', {'user':user, 'salaries':sobj})



def pay_fee(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = Student.objects.get(username=key)
            feeobj = Fee.objects.filter(student=user)
        except Student.DoesNotExist:
            return redirect('home')
    
    if request.method == 'POST':
        paid = int(request.POST['paid'])
        payment = request.FILES.get('payment')
        
        # Check if the student has made a recent payment
        recent_payment = Fee.objects.filter(student=user, date__gte=timezone.now() - timezone.timedelta(days=30)).exists()
        if recent_payment:
            messages.error(request, 'Payment Already Exist')
            return redirect('pay_fee') 
        
        actual_fee = user.sfee
        due = actual_fee - paid
        
        fee_payment = Fee(student=user, paid=paid, due=due, payment=payment)
        fee_payment.save()
        messages.success(request, 'Fee Paid')
        return redirect('pay_fee') 
 
    return render(request, 'pay_fee.html', {'user':user, 'fees':feeobj})


def view_fee(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
        except AcedemiaAdmin.DoesNotExist:
            return redirect('home')
    fee = Fee.objects.all()
    return render(request, 'view_fee.html',{'user':user, 'fees':fee})


def approvefee(request, id):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = AcedemiaAdmin.objects.get(username=key)
        except AcedemiaAdmin.DoesNotExist:
            return redirect('home')
    obj = Fee.objects.get(id=id)
    obj.status = True
    obj.save()

    return redirect('view_fee')

def logout(request):
    request.session.flush()
    return redirect('home')
