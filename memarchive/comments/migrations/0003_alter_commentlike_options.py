# Generated by Django 5.0.7 on 2024-08-04 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentlike',
            options={'verbose_name': 'comment like', 'verbose_name_plural': 'comment likes'},
        ),
    ]
