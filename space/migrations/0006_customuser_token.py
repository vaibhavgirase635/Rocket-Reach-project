# Generated by Django 4.1.3 on 2022-12-29 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0005_pricing_plan_purchased_subcription_delete_myfile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='token',
            field=models.IntegerField(default=5),
        ),
    ]
