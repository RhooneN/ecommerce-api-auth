from django.contrib import admin
from .models import Profile

#admin.site.register(Profile)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['bio', 'location', 'profile_picture']
