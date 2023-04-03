# Generated by Django 4.1.7 on 2023-03-31 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_loanrequest_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='approvalDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='payday',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='loanrequest',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
