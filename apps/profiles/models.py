from django.db import models
from users.models import Metadata_Abstract_Info
from django.contrib.auth.models import User


class prfl_profile(Metadata_Abstract_Info):
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
        ('other','other')
    )
    
    profile_id = models.BigAutoField(primary_key=True)
    profile_name = models.CharField("Profile name", blank=False, max_length=200, null=False, unique=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profile_pic/', height_field=None, width_field=None, max_length=200)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField("Gender", choices=GENDER, null=True, blank=True, max_length=50)
    user = models.OneToOneField(User , related_name='user_profile', on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = "prfl_profile"
        verbose_name = ('Profile')
        verbose_name_plural = ('Profiles')