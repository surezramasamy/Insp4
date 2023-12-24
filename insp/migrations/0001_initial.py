# Generated by Django 4.1.7 on 2023-11-19 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkpoint', models.CharField(blank=True, max_length=256, null=True)),
                ('uom', models.CharField(blank=True, max_length=256, null=True)),
                ('spec_min', models.FloatField(blank=True, null=True)),
                ('spec_max', models.FloatField(blank=True, null=True)),
                ('actual', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True, null=True)),
                ('Actual', models.FloatField(blank=True, null=True)),
                ('check_point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insp.check')),
            ],
        ),
        migrations.AddField(
            model_name='check',
            name='part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insp.part'),
        ),
    ]
