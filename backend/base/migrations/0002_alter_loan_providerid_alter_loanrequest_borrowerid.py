# Generated by Django 4.1.7 on 2023-03-31 00:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='providerId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loanrequest',
            name='borrowerId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrower_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
