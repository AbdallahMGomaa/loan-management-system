# Generated by Django 4.1.7 on 2023-03-31 00:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_loan_providerid_alter_loanrequest_borrowerid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrequest',
            name='borrowerId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
