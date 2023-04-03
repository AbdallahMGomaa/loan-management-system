from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    DateField,
    FloatField,
    BooleanField,
    CharField,
    RelatedField
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        token['is_admin'] = user.is_superuser
        return token

class FundSerializer(ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'

class BankUserSerializer(ModelSerializer):
    class Meta:
        model = BankUser
        fields = ['id', 'username', 'role']


'''
id = models.AutoField(primary_key=True)
borrowerId = models.ForeignKey(BankUser, on_delete=models.CASCADE)
date = models.DateField(auto_now_add=True)
amount = models.FloatField()
terms = models.CharField(max_length=1000)
isApproved = models.BooleanField(default=False)
'''
class LoanSerializer(ModelSerializer):

    # borrowerId = RelatedField(source='id.borrowerId', read_only=True)
    # approvalDate = DateField(source='id.approvalDate', read_only=True)
    date = DateField(source='id.date', read_only=True)
    amount = FloatField(source='id.amount', read_only=True)
    terms = CharField(source='id.terms', read_only=True)
    isApproved = BooleanField(source='id.isApproved', read_only=True)


    class Meta:
        model = Loan
        fields = (
            'id',
            'date',
            'amount',
            'isApproved',
            'deadline',
            'interestRate',
            'payday',
            'isPaid',
            'minimumPayment',
            'maximumPayment',
            'approvalDate',
            'terms'
        )

class LoanRequestSerializer(ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = '__all__'

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
