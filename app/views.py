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
from .models import Message
from django.contrib.auth import get_user_model


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

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate the user
        user = CustomUser.objects.filter(email=email).first()
        if user:
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('profile')
            else:
                messages.error(request, 'Invalid password')
        else:
            messages.error(request, 'Email not found')

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



# View for listing jobs
def job_list(request):
    jobs = Job.objects.filter(is_approved=True)
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(title__icontains=query)
    return render(request, 'job_list.html', {'jobs': jobs})

# View for job details
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_approved=True)
    return render(request, 'job_detail.html', {'job': job})

# Merchant: Create job posting
@login_required
def create_job(request):
    if request.user.role != 'merchant':
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'create_job.html', {'form': form})

# Admin: Approve job postings
@login_required
def approve_jobs(request):
    if request.user.role != 'admin':
        return redirect('job_list')

    jobs = Job.objects.filter(is_approved=False)
    return render(request, 'approve_jobs.html', {'jobs': jobs})

@login_required
def approve_job(request, job_id):
    if request.user.role != 'admin':
        return redirect('job_list')

    job = get_object_or_404(Job, id=job_id)
    job.is_approved = True
    job.save()
    return redirect('approve_jobs')

@login_required
def delete_job(request, job_id):
    if request.user.role == 'admin' or request.user == Job.objects.get(id=job_id).created_by:
        job = get_object_or_404(Job, id=job_id)
        job.delete()
    return redirect('job_list')



User = get_user_model()

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'inbox.html', {'messages': messages})

@login_required
def sent_messages(request):
    messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'sent_messages.html', {'messages': messages})

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        content = request.POST['content']
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('inbox')
    return render(request, 'send_message.html', {'receiver': receiver})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return render(request, 'message_detail.html', {'message': message})

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('/')
    total_users = CustomUser.objects.filter(role='user').count()
    total_merchants = CustomUser.objects.filter(role='merchant').count()
    total_jobs = Job.objects.count()
    return render(request, 'admin_dashboard.html', {
        'total_users': total_users,
        'total_merchants': total_merchants,
        'total_jobs': total_jobs
    })

@login_required
def manage_users(request):
    if request.user.role != 'admin':
        return redirect('/')
    users = CustomUser.objects.filter(role='user')
    return render(request, 'manage_users.html', {'users': users})

@login_required
def delete_user(request, user_id):
    if request.user.role != 'admin':
        return redirect('/')
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('manage_users')

@login_required
def manage_merchants(request):
    if request.user.role != 'admin':
        return redirect('/')
    merchants = CustomUser.objects.filter(role='merchant')
    return render(request, 'manage_merchants.html', {'merchants': merchants})

@login_required
def delete_merchant(request, merchant_id):
    if request.user.role != 'admin':
        return redirect('/')
    merchant = get_object_or_404(CustomUser, id=merchant_id)
    merchant.delete()
    return redirect('manage_merchants')

@login_required
def manage_jobs(request):
    if request.user.role != 'admin':
        return redirect('/')
    jobs = Job.objects.all()
    return render(request, 'manage_jobs.html', {'jobs': jobs})

@login_required
def delete_job_admin(request, job_id):
    if request.user.role != 'admin':
        return redirect('/')
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('manage_jobs')
