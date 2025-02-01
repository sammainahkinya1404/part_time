from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    # Built-in Django Admin Panel
    path('admin/', admin.site.urls),

    # Home and Authentication
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # User & Merchant Profiles
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('resume/upload/', upload_resume, name='upload_resume'),
    path('resume/download/', download_resume, name='download_resume'),

    # Job Listings
    path('create_job/', create_job, name='create_job'),
    path('job_list/', job_list, name='job_list'),
    path('manage_jobs/', manage_jobs, name='manage_jobs'),
    path('delete_job/', delete_job, name='delete_job'),

    # Messaging
    path('inbox/', inbox, name='inbox'),
    path('sent_messages/', sent_messages, name='sent_messages'),
    path('send_message/', send_message, name='send_message'),
    path('message_detail/<int:message_id>/', message_detail, name='message_detail'),

    # ✅ Custom Admin Panel (Separate from Django’s built-in admin)
    path('custom-admin/dashboard/', admins_dashboard, name='admins_dashboard'),
    path('manage_users/', manage_users, name='manage_users'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('manage_merchants', manage_merchants, name='manage_merchants'),
    path('delete_merchant/<int:merchant_id>/', delete_merchant, name='delete_merchant'),
    path('manage_jobs/', manage_jobs, name='manage_jobs'),

    # Job application
    path('job_apply/', job_apply, name='job_apply'),
    path('view_applicants/', view_applicants, name='view_applicants'),
    path('download_resume1/<str:applicant_username>/', download_resume1, name='download_resume1'),
    path('assign_task/', assign_task, name='assign_task'),
    path('my_applications/', my_applications, name='my_applications'),
    path('my_tasks/', my_tasks, name='my_tasks'),
    path('track_assigned_tasks/', track_assigned_tasks, name='track_assigned_tasks'),
]
