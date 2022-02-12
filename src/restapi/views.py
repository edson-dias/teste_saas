from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, CompanySerializer
from .models import User, Company


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def company_user(self, request):
        company_id = request.query_params.get('company_id', None)
        if not company_id:
            return Response({'error': 'company_id is required'}, status=400)
        queryset = User.objects.filter(company__id=company_id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def new(self, request):
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name', ''),
            'email': request.data.get('email', ''),
            'password': request.data.get('password')
        }
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(serializer.data, status=201)
    

class CompanyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user_id = request.user.id
        queryset = Company.objects.filter(user__id=user_id)
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def new(self, request):
        data = {
            'corporate_name': request.data.get('corporate_name'),
            'trade_name': request.data.get('trade_name'),
            'cnpj': request.data.get('cnpj'),
            'user': request.data.get('user')
        }
        serializer = CompanySerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(serializer.data, status=201)
