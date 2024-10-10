from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Add User model to admin.
admin.site.register(User, UserAdmin)