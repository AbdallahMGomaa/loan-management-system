from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('fund/',views.FundAPI.as_view()),
    path('user/', views.UserAPI.as_view()),
    path('loan/request/', views.LoanRequestAPI.as_view()),
    path('loan/approve/', views.LoanAPI.as_view()),
    path('loan/payment/', views.PaymentAPI.as_view())
]

