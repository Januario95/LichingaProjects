from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProjectViewSet,
    projects_view, project_detail_view, fish_selling,
    bank_statement, bank_statement_api, venda_de_feijao,
    fish_to_teachers, gergelim_selling, beans_selling,
    fish_lichinga, fish_selling_meponda,
)

app_name = 'app'

router = DefaultRouter()
router.register('projects', ProjectViewSet)

urlpatterns = [
    # APIs
    path('api/', include(router.urls)),
    
    # Views
    path('venda-de-feijao-2/', venda_de_feijao, name='venda_de_feijao_2'),
    path('venda-de-feijao/', beans_selling, name='beans_selling'),
    path('venda-de-gergelim/', gergelim_selling, name='gergelim_selling'),
    path('fish-lichinga/', fish_lichinga, name='fish_lichinga'),
    path('fish-to-teachers/', fish_to_teachers, name='fish_to_teachers'),
    path('projects/', projects_view, name='projects'),
    path('', projects_view, name='projects-2'),
    path('project/<str:project_name>/', project_detail_view, 
         name='project_detail'),
    path('fish-selling/', fish_selling, name='fish_selling'),
    path('fish-selling-meponda/', fish_selling_meponda, name='fish_selling_meponda'),
    path('bank-statement/', bank_statement, name='bank_statement'),
    path('api/bank_statement/<str:start_date>/<str:end_date>/', bank_statement_api),
]