from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AuditLog(models.Model):
    """
    Modelo para registrar todas as ações dos usuários no sistema.
    Fornece rastreabilidade e auditoria de segurança.
    """
    
    # Tipos de ação
    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('VIEW', 'Visualização'),
        ('CREATE', 'Criação'),
        ('UPDATE', 'Atualização'),
        ('DELETE', 'Exclusão'),
        ('ACCESS_DENIED', 'Acesso Negado'),
        ('ERROR', 'Erro'),
    ]
    
    # Níveis de severidade
    SEVERITY_CHOICES = [
        ('INFO', 'Informação'),
        ('WARNING', 'Aviso'),
        ('ERROR', 'Erro'),
        ('CRITICAL', 'Crítico'),
    ]
    
    # Informações do usuário
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name='Usuário'
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Nome de usuário',
        help_text='Armazena o username mesmo se o usuário for deletado'
    )
    
    # Informações da ação
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='Ação'
    )
    description = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição detalhada da ação'
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='INFO',
        verbose_name='Severidade'
    )
    
    # Informações da requisição
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Endereço IP'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='User Agent',
        help_text='Informações do navegador/dispositivo'
    )
    path = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='URL acessada'
    )
    method = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Método HTTP'
    )
    
    # Dados adicionais
    extra_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Dados adicionais',
        help_text='Informações extras em formato JSON'
    )
    
    # Timestamp
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data e Hora',
        db_index=True
    )
    
    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.username} - {self.get_action_display()} - {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}"
    
    @property
    def formatted_timestamp(self):
        """Retorna timestamp formatado em português"""
        return self.timestamp.strftime('%d/%m/%Y às %H:%M:%S')
    
    @property
    def severity_badge_class(self):
        """Retorna classe CSS do Bootstrap para badge de severidade"""
        severity_map = {
            'INFO': 'bg-info',
            'WARNING': 'bg-warning',
            'ERROR': 'bg-danger',
            'CRITICAL': 'bg-dark',
        }
        return severity_map.get(self.severity, 'bg-secondary')
    
    @property
    def action_icon(self):
        """Retorna ícone do Bootstrap para o tipo de ação"""
        icon_map = {
            'LOGIN': 'bi-box-arrow-in-right',
            'LOGOUT': 'bi-box-arrow-right',
            'VIEW': 'bi-eye',
            'CREATE': 'bi-plus-circle',
            'UPDATE': 'bi-pencil-square',
            'DELETE': 'bi-trash',
            'ACCESS_DENIED': 'bi-shield-x',
            'ERROR': 'bi-exclamation-triangle',
        }
        return icon_map.get(self.action, 'bi-info-circle')
