from django.contrib import admin
from .models import Group, UserProfile, Student, GroupAdmin

admin.site.register(Group)
admin.site.register(UserProfile)
admin.site.register(Student)
admin.site.register(GroupAdmin)