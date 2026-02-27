from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('gestao/dashboard/', views.gestao_dashboard, name='gestao_dashboard'),
    path('gestao/logs/', views.audit_logs_view, name='audit_logs'),
    path('paineis/', views.paineis_view, name='paineis_bi'),
    path('paineis/<int:painel_id>/', views.paineis_view, name='paineis_bi_detalhe'),
]
