from django.urls import path,include
from my_app.views import EmployeeCR, EmployeeRUD, UserRegistrationAPIView, UserLoginAPIView
#from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('list',EmployeeCR.as_view(),name='Employee-list'),
    path('list/<int:pk>',EmployeeRUD.as_view(), name="employee-details"),
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
]
