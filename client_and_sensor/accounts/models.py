from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import uuid

# GroupAdmin represents a professor or group leader
class GroupAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name

# Group represents a group or organization, managed by a GroupAdmin
class Group(models.Model):
    group_id = models.CharField(max_length=20, unique=True, primary_key=True)
    group_name = models.CharField(max_length=100)
    user_count = models.IntegerField(default=0)
    max_users = models.IntegerField(default=10)  # Limit number of students per group

    def __str__(self):
        return self.group_name

# UserProfile extends the User model to include group association
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

# Student represents a student in a group, includes email confirmation
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group_admin = models.ForeignKey(GroupAdmin, on_delete=models.CASCADE)  # Link to GroupAdmin
    confirmation_token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_confirmed = models.BooleanField(default=False)

    def send_confirmation_email(self):
        subject = "Confirm your email"
        message = f"Hi {self.user.username},\n\nPlease confirm your registration by clicking the link below:\nhttp://127.0.0.1:8000/accounts/confirm/{self.confirmation_token}\n\nThank you!"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.user.email], fail_silently=False)

    def __str__(self):
        return self.user.username