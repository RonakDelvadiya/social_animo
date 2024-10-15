from django.contrib import admin
from .models import *

# Register your models here.

class usr_email_verification_admin(admin.ModelAdmin):
    list_display = ("verification_id","generated_otp","email","active","created_at","modified_at")
    search_fields = ('email',)


admin.site.register(usr_email_verification,usr_email_verification_admin)
