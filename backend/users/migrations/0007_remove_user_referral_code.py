# Generated by Django 4.1 on 2023-03-08 08:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_user_referral_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="referral_code",
        ),
    ]
