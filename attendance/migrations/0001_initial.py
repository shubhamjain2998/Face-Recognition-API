# Generated by Django 3.0.6 on 2020-05-23 10:41

import attendance.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empId', models.IntegerField()),
                ('check_in', models.TimeField()),
                ('check_out', models.TimeField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depId', models.IntegerField(unique=True)),
                ('DeptName', models.CharField(max_length=60)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('orgType', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=12)),
                ('staffcount', models.IntegerField()),
                ('logo', models.ImageField(blank=True, null=True, storage=attendance.models.MediaFileSystemStorage(), upload_to='companyLogo//')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empId', models.IntegerField(unique=True)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('firstName', models.CharField(max_length=60)),
                ('lastName', models.CharField(max_length=60)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('phone', models.CharField(max_length=20)),
                ('readEmp', models.BooleanField(default=False)),
                ('addEmp', models.BooleanField(default=False)),
                ('readAtt', models.BooleanField(default=False)),
                ('addAtt', models.BooleanField(default=False)),
                ('readDept', models.BooleanField(default=False)),
                ('addDept', models.BooleanField(default=False)),
                ('idType', models.CharField(choices=[('AC', 'Adhaar Card'), ('PC', 'PAN Card'), ('PP', 'Passport'), ('DL', 'Driving License')], max_length=2)),
                ('idProof', models.CharField(max_length=20, unique=True)),
                ('profileImg', models.ImageField(blank=True, null=True, storage=attendance.models.MediaFileSystemStorage(), upload_to='profilePics//')),
                ('role', models.CharField(max_length=30)),
                ('deptId', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='attendance.Department')),
                ('emailId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('orgId', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='attendance.Organization')),
            ],
        ),
    ]
