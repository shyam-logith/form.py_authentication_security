from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import StudentForm


def student_list(request):

    students = Student.objects.all()

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('student_list')

    else:
        form = StudentForm()

    return render(request, 'students/student_list.html', {
        'students': students,
        'form': form
    })


# Main Login
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('student_list')

        else:

            return render(request, 'students/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'students/login.html')


# Admin authentication before Update
def admin_login(request, id):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Store authentication for this update
            request.session['update_authenticated'] = True

            return redirect('update_student', id=id)

        else:

            return render(request, 'students/admin_login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'students/admin_login.html')


# Update Student
@login_required
def update_student(request, id):

    # Check admin authentication
    if not request.session.get('update_authenticated'):

        return redirect('admin_login', id=id)

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            # Remove authentication after update
            request.session.pop('update_authenticated', None)

            return redirect('student_list')

    else:

        form = StudentForm(instance=student)

    return render(request, 'students/update_student.html', {
        'form': form,
        'student': student
    })


# Delete Student
@login_required
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    student.delete()

    return redirect('student_list')
