# Generated by Django 4.1.7 on 2023-12-11 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insp', '0020_rename_actual_1_inspection_actual_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='Actual',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
