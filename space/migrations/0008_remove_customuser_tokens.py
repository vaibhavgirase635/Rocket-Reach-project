# Generated by Django 4.1.3 on 2022-12-29 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0007_rename_token_customuser_tokens'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='tokens',
        ),
    ]