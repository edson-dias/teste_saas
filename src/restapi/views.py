from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer, CompanySerializer
from .models import User, Company


class UserViewSet(viewsets.ViewSet):
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

    @action(detail=False, methods=['get'])
    def members(self, request):
        company_id = request.query_params.get('company_id', None)
        if not company_id:
            return Response({'error': 'company_id is required'}, status=400)
        queryset = User.objects.filter(company__id=company_id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    