from celery import shared_task
from .models import Company
from .views import get_company_data_from_external_api


@shared_task
def periodic_companies_maintenance():
    companies = [obj for obj in Company.objects.all() if obj.is_necessary_to_check]
    updated_ids = []
    try:
        for company in companies:
            infos = get_company_data_from_external_api(company.cnpj)
            company.update_company(infos['nome'], infos['fantasia'], infos['situacao'])
            updated_ids.append(company.id)
        return updated_ids
    except Exception as e:
        return {'error': str(e)}

