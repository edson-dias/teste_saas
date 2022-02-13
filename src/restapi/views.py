import requests
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, CompanySerializer
from .models import User, Company


class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny,]
    def create(self, request):
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
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='companies', url_name='companies')
    def get_logged_user_companies(self, request):
        user_id = request.user.id
        queryset = Company.objects.filter(user__id=user_id)
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_extra_action_url_map(self):
        return []
    

class CompanyViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny,]
    
    def create(self, request):
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

    @action(detail=True, methods=['get'], url_path='members', url_name='members', permission_classes=[IsAuthenticated])
    def get_members_from_company(self, request, pk=None):
        queryset = User.objects.filter(company__id=pk)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='members/registry', url_name='registry-member', permission_classes=[IsAuthenticated])
    def registry_member_in_company(self, request):
        company_id = request.data.get('company_id', None)
        user_id = request.data.get('user_id', None)
        if not company_id or not user_id:
            return Response({'error': 'company_id and user_id are required'}, status=400)
        company = get_object_or_404(Company, pk=company_id)
        user = get_object_or_404(User, pk=user_id)
        company.user.add(user)
        return Response({'message': 'success'}, status=200)
    
    def get_extra_action_url_map(self):
        return []


def get_company_data_from_external_api(cnpj):
    entrypoint = 'https://receitaws.com.br/v1/'
    
    url = f'{entrypoint}cnpj/{cnpj}'
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        data = {
            'nome': response['nome'],
            'fantasia': response['fantasia'],
            'situacao': response['situacao']
        }
        return data
    else:
       raise Exception('Não foi possível obter os dados da empresa')