from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from my_app.serializer import EmployeeSerializer
from my_app.models import Employee
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.




class EmployeeCR(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        details = Employee.objects.all()
        serializer = EmployeeSerializer(details,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class EmployeeRUD(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request,pk):
        try:
            detail = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({'Error':'Movie does not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(detail)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        detail = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(detail,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        detail = Employee.objects.get(pk=pk)
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if username and password:
            if User.objects.filter(username=username).exists():
                return Response({"message": "Username already exists. Please choose a different one."},
                                status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully.",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response({"message": "Username and password are required."},
                        status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful.",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response({"message": "Invalid credentials."},
                        status=status.HTTP_401_UNAUTHORIZED)