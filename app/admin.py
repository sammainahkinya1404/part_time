from django.contrib import admin

# Register your models here.
from app.models import CustomUser, Job, Message
 
admin.site.register(CustomUser)
admin.site.register(Job)
admin.site.register(Message)