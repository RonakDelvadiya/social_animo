from django.db import models
from profiles.models import prfl_profile

# Create your models here.

class frnd_friends_mapping(models.Model):
    mapping_id = models.BigAutoField(primary_key=True)
    profile_id = models.OneToOneField(prfl_profile, related_name='profile_friends_mapping', on_delete=models.CASCADE)
    friends_id = models.ManyToManyField(prfl_profile, related_name='friends_mapping_with_profile', blank=True)

    class Meta:
        db_table = "frnd_friends_mapping"
        verbose_name = ('Friend mapping')
        verbose_name_plural = ('Friends mapping')