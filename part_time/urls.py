from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    # Built-in Django Admin Panel
    path('admin/', admin.site.urls),

    # Home and Authentication
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login_view/', login_view, name='login_view'),

    # User & Merchant Profiles
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('resume/upload/', upload_resume, name='upload_resume'),
    path('resume/download/', download_resume, name='download_resume'),

    # Job Listings
    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),
    path('jobs/create/', create_job, name='create_job'),
    path('jobs/approve/', approve_jobs, name='approve_jobs'),
    path('jobs/approve/<int:job_id>/', approve_job, name='approve_job'),
    path('jobs/delete/<int:job_id>/', delete_job, name='delete_job'),

    # Messaging
    path('messages/inbox/', inbox, name='inbox'),
    path('messages/sent/', sent_messages, name='sent_messages'),
    path('messages/send/<int:receiver_id>/', send_message, name='send_message'),
    path('messages/<int:message_id>/', message_detail, name='message_detail'),

    # ✅ Custom Admin Panel (Separate from Django’s built-in admin)
    path('custom-admin/dashboard/', admins_dashboard, name='admins_dashboard'),
    path('manage_users/', manage_users, name='manage_users'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('manage_merchants', manage_merchants, name='manage_merchants'),
    path('delete_merchant/<int:merchant_id>/', delete_merchant, name='delete_merchant'),
    path('manage_jobs/', manage_jobs, name='manage_jobs'),
    path('delete_job_admin/<int:job_id>/', delete_job_admin, name='delete_job_admin'),
]
