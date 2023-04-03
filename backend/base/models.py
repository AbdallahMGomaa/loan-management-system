from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import BankUserManager
from django.utils import timezone


class BankUser(AbstractUser, PermissionsMixin):
    PROVIDER = 1
    CUSTOMER = 2
    EMPLOYEE = 3
    CHOICES = (
        (PROVIDER, 'provider'),
        (CUSTOMER, 'customer'),
        (EMPLOYEE, 'employee')
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.IntegerField(choices=CHOICES)
    username = models.CharField(unique=True, max_length=50)
    objects = BankUserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = None # type: ignore
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.username

class LoanRequest(models.Model):
    id = models.AutoField(primary_key=True)
    borrowerId = models.ForeignKey(BankUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField()
    terms = models.CharField(max_length=1000)
    isApproved = models.BooleanField(default=False)

class Loan(models.Model):
    id = models.OneToOneField(LoanRequest, on_delete=models.CASCADE, primary_key=True)
    providerId = models.ForeignKey(BankUser, on_delete=models.CASCADE)
    approvalDate = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    interestRate = models.FloatField()
    payday = models.DateField(null=True)
    isPaid = models.BooleanField(default=False)
    minimumPayment = models.FloatField()
    maximumPayment = models.FloatField()

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

class Fund(models.Model):
    provider = models.OneToOneField(BankUser, on_delete=models.CASCADE, primary_key=True)
    budget = models.FloatField(default=0) # type: ignore



