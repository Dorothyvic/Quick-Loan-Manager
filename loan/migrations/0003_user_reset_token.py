# Generated by Django 4.1.7 on 2023-03-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0002_alter_user_managers_user_is_active_user_is_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
