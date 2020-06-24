# Generated by Django 3.0.6 on 2020-06-01 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_auto_20200526_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='leave',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='empId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Account'),
        ),
    ]