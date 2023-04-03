from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Fund
from .permissions import *

from .serializers import *

from django.db.models import Sum
from django.utils.timezone import make_aware

from datetime import datetime

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class FundAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AuthorizeProvider]

    def post(self, request):
        data = request.data
        try:
            loanBudget = float(data['budget'])
        except:
            return Response({"error":"budget not found"},status=400)
        user = request.user
        try:
            fund = Fund.objects.get(provider=user)
        except:
            fund = Fund.objects.create(provider=user)
        if loanBudget>0:
            fund.budget += loanBudget
            fund.save()
        else:
            return Response({'error':'fund amound must be positive'})
        serializer = FundSerializer(fund)
        return Response(serializer.data)

    def get(self, request):
        user = request.user
        loans = Loan.objects.select_related('id').filter(providerId=user)
        fund = Fund.objects.get(provider=user)
        fundSerializer = FundSerializer(fund)
        loanSerializer = LoanSerializer(loans, many=True)
        return Response({'fund':fundSerializer.data,'loans':loanSerializer.data}, status=200)



class UserAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AuthorizeAdmin]

    def get(self, request):
        users = BankUser.objects.all()
        serializer = BankUserSerializer(users,many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data
        try:
            username = data['username']
            password = data['password']
            role = data['role']
            assert role in [BankUser.PROVIDER, BankUser.CUSTOMER, BankUser.EMPLOYEE]
        except:
            return Response({'error':'data is missing'}, status=400)
        try:
            user = BankUser.objects.create_user(username=username, password=password, role=role)
        except:
            return Response({'error':'user already exists'}, status=400)
        serializer = BankUserSerializer(user)
        return Response(serializer.data, status=200)

    def delete(self, request):
        data = request.data
        try:
            userId = data['id']
        except:
            return Response({'error':'data is missing'}, status=400)

        try:
            user = BankUser.objects.get(id=userId)
            if user.is_superuser:
                return Response({'error': 'cannot delete admin users'}, status=400)
            user.delete()
        except:
            return Response({'error':'user is not found'}, status=400)
        return Response({'message': 'user deleted successfully'}, status=200)



class LoanRequestAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AuthorizeCustomer]

    def get(self, request):
        user = request.user
        loanRequests = LoanRequest.objects.filter(borrowerId=user)
        loans = Loan.objects.filter(id__borrowerId=user)
        loanRequestSerializer = LoanRequestSerializer(loanRequests, many=True)
        loanSerializer = LoanSerializer(loans, many=True)
        return Response({'loanRequests':loanRequestSerializer.data, 'loans': loanSerializer.data}, status=200)

    def post(self, request):
        user = request.user
        data = request.data
        try:
            amount = float(data['amount'])
            terms = data['terms']
            assert amount > 0
        except:
            return Response({'error':'data is missing'}, status=400)
        loanRequest = LoanRequest.objects.create(borrowerId=user, amount=amount, terms=terms)
        loanRequest.save()
        serializer = LoanRequestSerializer(loanRequest)
        return Response(serializer.data, status=200)

    def delete(self, request):
        data = request.data
        try:
            loanRequestId = data['loanRequestId']
        except:
            return Response({'error':'data is missing'}, status=400)
        try:
            loanRequest = LoanRequest.objects.get(id=loanRequestId)
            if loanRequest.isApproved:
                return Response({'error':'request was already approved'}, status=400)
            loanRequest.delete()
        except:
            return Response({'error':'loan request is not found'}, status=400)
        return Response({'message':'request deleted successfully'})



class LoanAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AuthorizeEmployee]

    def get(self, request):
        loanRequests = LoanRequest.objects.filter(isApproved=False)
        serializer = LoanRequestSerializer(loanRequests, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data
        try:
            loanRequestId = data['loanRequestId']
            interestRate = float(data['interestRate'])
            assert interestRate > 0 and interestRate < 1
            deadline = data['deadline']
            deadline = datetime.date(make_aware(datetime.strptime(deadline, '%Y-%m-%d')))
            today = datetime.date(datetime.now())
            if deadline < today:
                return Response({'error': 'date cant be in the past'})
            providerId = data['providerId']
            minimumPayment = float(data['minimumPayment'])
            maximumPayment = float(data['maximumPayment'])

        except:
            return Response({'error':'data is missing or incorrect'}, status=400)
        try:
            loanRequest = LoanRequest.objects.get(id=loanRequestId)
            assert loanRequest.isApproved == False
            provider = BankUser.objects.get(id=providerId)
            assert provider.role == BankUser.PROVIDER
            fund = Fund.objects.get(provider=provider)
        except:
            return Response({'error':'data was not found'}, status=400)

        try:
            assert minimumPayment <= loanRequest.amount
            assert minimumPayment > 0
            assert maximumPayment<= loanRequest.amount
            assert maximumPayment > minimumPayment
        except:
            return Response({'error':'invalid payment limitation range'}, status=400)
        if fund.budget >= loanRequest.amount:
            loanRequest.isApproved = True
            loan = Loan.objects.create(
                id=loanRequest,
                providerId=provider,
                deadline=deadline,
                interestRate=interestRate,
                minimumPayment=minimumPayment,
                maximumPayment=maximumPayment
            )
            fund.budget -= loanRequest.amount
            loanRequest.save()
            loan.save()
            fund.save()
        else:
            return Response({'error':'budget is not enough'}, status=400)
        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=200)


class PaymentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AuthorizeCustomer]

    def get(self, request):
        user = request.user
        loanRequests = LoanRequest.objects.filter(borrowerId=user, isApproved=True)
        loans = Loan.objects.filter(id__in=loanRequests)
        payments = Payment.objects.filter(loan__in=loans)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        user = request.user
        data = request.data
        try:
            paymentAmount = float(data['paymentAmount'])
            loanId = data['loanId']
            assert paymentAmount > 0
        except:
            return Response({'error':'data is missing'}, status=400)
        try:
            loan = Loan.objects.get(id=loanId)
            assert loan.id.borrowerId == user
        except:
            return Response({'error':'invalid loan id'}, status=400)
        if loan.isPaid:
            return Response({'error':'loan is already paid'}, status=400)
        if paymentAmount > loan.maximumPayment:
            return Response({'error':'payment is more than maximum payment allowed'}, status=400)
        if paymentAmount < loan.minimumPayment:
            return Response({'error':'payment is less than minimum payment allowed'}, status=400)

        totalPayments = Payment.objects.filter(loan=loan).aggregate(Sum('amount'))
        totalAmount = totalPayments['amount__sum'] or 0
        if loan.id.amount*(1+loan.interestRate) == totalAmount+paymentAmount:
            loan.isPaid = True
            loan.payday = timezone.now()
            loan.save()
        elif loan.id.amount*(1+loan.interestRate) < totalAmount+paymentAmount:
            return Response({'error':'payment is more than what is required'}, status=400)
        payment = Payment.objects.create(loan=loan, amount=paymentAmount)
        payment.save()
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=200)
