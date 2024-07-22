from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, StudentRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Group, UserProfile, Student, GroupAdmin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse  
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required, user_passes_test



def send_test_email(request):
    subject = 'Test Email'
    message = 'This is a test email from Django.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['recipient@example.com']  # Replace with a test recipient email
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponse("Test email sent successfully")

def register(request):
    """
    Handle registration of a new user. Creates a UserProfile linked to a Group.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data.get('group')
            UserProfile.objects.create(user=user, group=group)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def student_register(request, group_id):
    """
    Handle student registration for a specific GroupAdmin. Sends a confirmation email to the student.
    """
    group_admin = get_object_or_404(GroupAdmin, id=group_id)
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            student = Student.objects.create(user=user, group_admin=group_admin)
            student.send_confirmation_email()
            messages.success(request, 'Registration successful. Please check your email to confirm.')
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts/student_register.html', {'form': form, 'group_admin': group_admin})

def confirm_email(request, token):
    """
    Handle email confirmation for a student using a unique token.
    """
    student = get_object_or_404(Student, confirmation_token=token)
    student.is_confirmed = True
    student.save()
    messages.success(request, 'Email confirmed successfully!')
    return redirect('login')



def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')

def login_view(request):
    """
    Handle user login. Redirects to the dashboard upon successful authentication.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')  # Get the 'next' parameter from the request
            if next_url:
                return redirect(next_url)  # Redirect to the original URL
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    next_url = request.GET.get('next', '')
    return render(request, 'accounts/login.html', {'next': next_url})

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """
    Render the user dashboard. Requires login.
    """
    return render(request, 'accounts/dashboard.html')

@login_required
def delete_student(request, student_id):
    """
    Allow GroupAdmin to delete a student. Requires login.
    """
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('dashboard')


#Custom Groupadmin
@login_required
def view_students(request):
    group_admin = request.user.groupadmin  # Assuming request.user is authenticated GroupAdmin
    students = Student.objects.filter(group_admin=group_admin)
    return render(request, 'accounts/view_students.html', {'students': students})

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.user != student.group_admin.user:
        return render(request, 'accounts/access_denied.html')  # Return access denied page if not authorized
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('view_students')
    return render(request, 'accounts/delete_student_confirm.html', {'student': student})

#Dashboard
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')