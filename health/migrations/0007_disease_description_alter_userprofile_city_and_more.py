# Generated by Django 5.1.7 on 2025-03-20 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0006_userprofile_disease'),
    ]

    operations = [
        migrations.AddField(
            model_name='disease',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='street',
            field=models.CharField(max_length=25),
        ),
    ]
