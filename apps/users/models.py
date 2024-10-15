from django.db import models

# Create your models here.

class Metadata_Abstract_Info(models.Model):
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        abstract=True


class usr_email_verification(Metadata_Abstract_Info):
    verification_id = models.BigAutoField(primary_key=True)
    generated_otp = models.CharField("OTP", blank=False, max_length=12, null=False, unique=True)
    email = models.EmailField("Email", max_length = 254,blank=False,null=False)

    class Meta:
        db_table = "usr_email_verification"
        verbose_name = ('Email verification')

    # def __unicode__(self):
    #     str(self.verification_id)

    # def __str__(self):
    #     str(self.verification_id)