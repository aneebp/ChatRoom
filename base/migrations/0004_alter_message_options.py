# Generated by Django 4.2.3 on 2024-09-26 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['update', 'create']},
        ),
    ]
