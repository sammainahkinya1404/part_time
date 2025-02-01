from django.shortcuts import *
# import requests
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib.auth.hashers import make_password
# from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ProfileForm, ResumeUploadForm
from .forms import JobForm
from .forms import MessageForm
from .models import Message
from django.contrib.auth import get_user_model

def home(request):
    return render(request, 'home.html')
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        # Check if user already exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        # Create user
        user = CustomUser(
            username=username,
            email=email,
            password=make_password(password),
            role=role
        )
        user.save()

        # Log the user in after registration
        login(request, user)
        return redirect('/')

    return render(request, 'register.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']  # Email for users, Username for superusers
        password = request.POST['password']

        user = CustomUser.objects.filter(email=identifier).first()

        if user:
            authenticated_user = authenticate(username=user.username, password=password)
        else:
            authenticated_user = authenticate(username=identifier, password=password)

        if authenticated_user:
            login(request, authenticated_user)

            # ✅ Redirect superusers to new custom admin dashboard URL
            if authenticated_user.is_superuser:
                return redirect('admins_dashboard')

            return redirect('profile')

        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ResumeUploadForm(instance=request.user)
    return render(request, 'upload_resume.html', {'form': form})

@login_required
def download_resume(request):
    if request.user.resume:
        with open(request.user.resume.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{request.user.username}_resume.pdf"'
            return response
    return redirect('profile')

@login_required
def job_apply(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        job = get_object_or_404(Job, title=job_title)
        message = request.POST.get('message')

        # Ensure the user has uploaded a resume
        if not request.user.resume:
            messages.error(request, "Please upload a resume before applying for jobs.")
            return redirect('profile')

        # Create the job application
        JobApplication.objects.create(job=job, applicant=request.user, message=message)
        messages.success(request, f"You have successfully applied for {job.title}.")
        return redirect('job_list')

    return redirect('job_list')


@login_required
def view_applicants(request):
    if request.user.role != 'merchant':
        return redirect('job_list')

    jobs = Job.objects.filter(created_by=request.user)
    return render(request, 'view_applicants.html', {'jobs': jobs})


@login_required
def download_resume1(request, applicant_username):
    applicant = get_object_or_404(User, username=applicant_username)
    if applicant.resume:
        with open(applicant.resume.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{applicant.username}_resume.pdf"'
            return response
    messages.error(request, "This applicant has not uploaded a resume.")
    return redirect('view_applicants')



# View for listing jobs
User = get_user_model()

# 📌 List Approved Jobs
@login_required
def job_list(request):
    jobs = Job.objects.all()
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(title__icontains=query)
    return render(request, 'job_list.html', {'jobs': jobs})




# 📌 Job Details
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_approved=True)
    return render(request, 'job_detail.html', {'job': job})



# 📌 Merchant: Create Job

@login_required
def create_job(request):
    if request.user.role != 'merchant':  # Only merchants can create jobs
        return redirect('job_list')

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        salary = request.POST['salary']
        location = request.POST['location']
        category = request.POST['category']

        Job.objects.create(
            title=title,
            description=description,
            salary=salary,
            location=location,
            category=category,
            created_by=request.user
        )
        messages.success(request, "Job created successfully.")
        return redirect('job_list')

    return render(request, 'create_job.html')

# 📌 Delete Job (Admin or Merchant Who Created It)

@login_required
def delete_job(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = Job.objects.get(id=job_id, created_by=request.user)
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('manage_jobs')

User = get_user_model()

# 📌 Inbox (Received Messages)
@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'inbox.html', {'messages': messages})

# 📌 Sent Messages
@login_required
def sent_messages(request):
    messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'sent_messages.html', {'messages': messages})

# 📌 Send Message (Dropdown List of Users)

@login_required
def send_message(request):
    users = User.objects.exclude(id=request.user.id)  # Get all users except the sender

    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('content')

        receiver = User.objects.get(id=receiver_id)
        Message.objects.create(sender=request.user, receiver=receiver, content=content)

        return redirect('inbox')  # Redirect to inbox after sending

    return render(request, 'send_message.html', {'users': users})

# 📌 View Message Details
@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return render(request, 'message_detail.html', {'message': message})
@login_required
def admins_dashboard(request):
    if not request.user.is_superuser:
        return redirect('/')

    total_users = CustomUser.objects.filter(role='user').count()
    total_merchants = CustomUser.objects.filter(role='merchant').count()
    total_jobs = Job.objects.count()
   

    return render(request, 'admins_dashboard.html', {
        'total_users': total_users,
        'total_merchants': total_merchants,
        'total_jobs': total_jobs,
        })

@login_required
def manage_users(request):
    users = CustomUser.objects.filter(role='user')
    return render(request, 'manage_users.html', {'users': users})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('manage_users')

@login_required
def manage_merchants(request):
    merchants = CustomUser.objects.filter(role='merchant')
    return render(request, 'manage_merchants.html', {'merchants': merchants})

@login_required
def delete_merchant(request, merchant_id):
    merchant = get_object_or_404(CustomUser, id=merchant_id)
    merchant.delete()
    return redirect('manage_merchants')

@login_required
def manage_jobs(request):
    if request.user.role != 'merchant':
        return redirect('job_list')
    jobs = Job.objects.filter(created_by=request.user)
    return render(request, 'manage_jobs.html', {'jobs': jobs})


from django.contrib.auth import logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def assign_task(request):
    if request.method == "POST":
        job_id = request.POST.get("job_id")
        applicant_id = request.POST.get("applicant_id")

        # Get the job and applicant objects
        job = get_object_or_404(Job, id=job_id, created_by=request.user)  # Ensure the merchant owns the job
        applicant = get_object_or_404(CustomUser, id=applicant_id)

        # Assign the job to the applicant
        job.assigned_user = applicant
        job.save()

        messages.success(request, f"Task successfully assigned to {applicant.username}!")
        return redirect("view_applicants")

    messages.error(request, "Invalid request.")
    return redirect("view_applicants")

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'my_applications.html', {'applications': applications})
@login_required
def my_tasks(request):
    assigned_jobs = Job.objects.filter(assigned_user=request.user)
    return render(request, 'my_tasks.html', {'assigned_jobs': assigned_jobs})
@login_required
def track_assigned_tasks(request):
    jobs = Job.objects.filter(created_by=request.user, assigned_user__isnull=False)
    return render(request, 'track_assigned_tasks.html', {'jobs': jobs})
