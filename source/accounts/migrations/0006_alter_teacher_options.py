# Generated by Django 4.2 on 2024-12-22 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_teacher_about_teacher_about_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['fullname'], 'verbose_name': 'Учитель', 'verbose_name_plural': 'Учителя'},
        ),
    ]
