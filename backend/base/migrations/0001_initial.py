# Generated by Django 4.1.7 on 2023-03-31 00:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('role', models.IntegerField(choices=[(1, 'provider'), (2, 'customer'), (3, 'employee')])),
                ('username', models.CharField(max_length=50, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoanRequest',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.FloatField()),
                ('terms', models.CharField(max_length=1000)),
                ('isApproved', models.BooleanField(default=False)),
                ('borrowerId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='borrower_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('provider', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('budget', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.loanrequest')),
                ('approvalDate', models.DateField(default=django.utils.timezone.now)),
                ('deadline', models.DateField()),
                ('interestRate', models.FloatField()),
                ('payday', models.DateField()),
                ('isPaid', models.BooleanField(default=False)),
                ('providerId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('loan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.loan')),
            ],
        ),
    ]
