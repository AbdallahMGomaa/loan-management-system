from django.contrib import admin

# Register your models here.

from .models import BankUser, Fund, Loan, Payment, LoanRequest

admin.site.register(BankUser)
admin.site.register(Fund)
admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(LoanRequest)
