# Generated by Django 3.2.7 on 2021-09-25 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usr_email_verification',
            fields=[
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('verification_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('generated_otp', models.CharField(max_length=12, unique=True, verbose_name='OTP')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('timeout_in_min', models.IntegerField(default=10)),
            ],
            options={
                'verbose_name': 'Email verification',
                'db_table': 'usr_email_verification',
            },
        ),
    ]
