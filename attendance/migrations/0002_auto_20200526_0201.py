# Generated by Django 3.0.6 on 2020-05-25 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='deptId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Department'),
        ),
        migrations.AlterField(
            model_name='account',
            name='firstName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='idProof',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='idType',
            field=models.CharField(choices=[('Adhaar Card', 'Adhaar Card'), ('PAN Card', 'PAN Card'), ('Passport', 'Passport'), ('Driving License', 'Driving License')], max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='lastName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='orgId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Organization'),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
