
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', register, name='register'),
    path('login_view/', login_view, name='login_view'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('resume/upload/', upload_resume, name='upload_resume'),
    path('resume/download/', download_resume, name='download_resume'),
    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),
    path('jobs/create/', create_job, name='create_job'),
    path('jobs/approve/', approve_jobs, name='approve_jobs'),
    path('jobs/approve/<int:job_id>/', approve_job, name='approve_job'),
    path('jobs/delete/<int:job_id>/', delete_job, name='delete_job'),
    path('messages/inbox/', inbox, name='inbox'),
    path('messages/sent/', sent_messages, name='sent_messages'),
    path('messages/send/<int:receiver_id>/', send_message, name='send_message'),
    path('messages/<int:message_id>/', message_detail, name='message_detail'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/', manage_users, name='manage_users'),
    path('admin/users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('admin/merchants/', manage_merchants, name='manage_merchants'),
    path('admin/merchants/delete/<int:merchant_id>/', delete_merchant, name='delete_merchant'),
    path('admin/jobs/', manage_jobs, name='manage_jobs'),
    path('admin/jobs/delete/<int:job_id>/', delete_job_admin, name='delete_job_admin'),
]
