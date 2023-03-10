# Generated by Django 4.1.3 on 2022-12-22 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0003_remove_myfile_description_remove_myfile_uploaded_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('stream', models.CharField(choices=[('Computer Science', 'Computer Science'), ('Business Administration', 'Business Administration'), ('Management', 'Management'), ('Marketing', 'Marketing'), ('Accounting', 'Accounting')], max_length=200)),
                ('school', models.CharField(max_length=200)),
                ('degree', models.CharField(choices=[('Bachelors', 'Bachelors'), ('Masters', 'Masters'), ('Associates', 'Associates'), ('Doctorates', 'Doctorates'), ('HighSchools', 'HighSchools')], max_length=200)),
                ('job_title', models.CharField(max_length=200)),
                ('skills', models.CharField(max_length=200)),
                ('experiance', models.IntegerField()),
                ('company', models.CharField(max_length=200, null=True)),
                ('phone', models.IntegerField(unique=True)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('linkdin', models.URLField(unique=True)),
                ('Twitter', models.URLField(null=True, unique=True)),
                ('github', models.URLField(null=True, unique=True)),
                ('alt_phone', models.IntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=100)),
                ('DOB', models.DateField()),
                ('profile_photo', models.ImageField(blank=True, upload_to='register/image')),
                ('location', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
