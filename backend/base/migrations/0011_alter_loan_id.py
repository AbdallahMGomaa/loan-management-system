# Generated by Django 4.1.7 on 2023-04-01 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_loan_maximumpayment_loan_minimumpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.loanrequest'),
        ),
    ]
