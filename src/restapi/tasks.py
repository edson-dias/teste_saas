from celery import shared_task
from .models import Company
from .views import get_company_data_from_external_api


@shared_task
def periodic_companies_maintenance():
    companies = [obj for obj in Company.objects.all() if obj.is_necessary_to_check]
    for company in companies:
        infos = get_company_data_from_external_api(company.cnpj)
        company.update_data(infos['nome'], infos['fantasia'], infos['situacao'])

