# Generated by Django 2.2.5 on 2020-12-05 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_code', models.CharField(max_length=16, null=True)),
                ('weld_method', models.CharField(max_length=32, null=True)),
                ('worker_code', models.CharField(max_length=32, null=True)),
                ('machine_code', models.CharField(max_length=32, null=True)),
                ('product_code', models.CharField(max_length=32, null=True)),
                ('process_card', models.CharField(max_length=256, null=True)),
                ('weld_current', models.FloatField(null=True)),
                ('weld_vol', models.FloatField(null=True)),
                ('weld_power', models.FloatField(null=True)),
                ('weld_speed', models.FloatField(null=True)),
                ('weld_gas', models.CharField(max_length=16, null=True)),
                ('app_test', models.NullBooleanField()),
                ('ray_test', models.NullBooleanField()),
                ('ray_test_prop', models.FloatField(null=True)),
                ('other_test', models.NullBooleanField()),
                ('other_test_method', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spot_code', models.CharField(max_length=32, null=True)),
                ('app_test_status', models.NullBooleanField()),
                ('app_inspector_code', models.CharField(default='', max_length=32, null=True)),
                ('app_defect_type', models.CharField(default='', max_length=32, null=True)),
                ('app_test_result', models.CharField(default='', max_length=16, null=True)),
                ('app_test_notes', models.TextField(default='', null=True)),
                ('ray_test_status', models.NullBooleanField()),
                ('ray_inspector_code', models.CharField(default='', max_length=32, null=True)),
                ('ray_defect_type', models.CharField(default='', max_length=32, null=True)),
                ('ray_test_result', models.CharField(default='', max_length=16, null=True)),
                ('ray_test_notes', models.TextField(default='', null=True)),
                ('app_defect_type_0', models.NullBooleanField()),
                ('app_defect_type_1', models.NullBooleanField()),
                ('app_defect_type_2', models.NullBooleanField()),
                ('app_defect_type_3', models.NullBooleanField()),
                ('app_defect_type_4', models.NullBooleanField()),
                ('app_defect_type_5', models.NullBooleanField()),
                ('task_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Data_manage.Task')),
            ],
        ),
    ]
