# Generated by Django 3.2.25 on 2025-04-27 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_organization_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
