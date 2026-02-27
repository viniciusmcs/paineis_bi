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


class CategoriaPainel(models.Model):
    """
    Categoria/Menu lateral para agrupar painéis Power BI.
    Ex: PAINÉIS GOV, PAINÉIS RH, etc.
    """
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome da Categoria'
    )
    icone = models.CharField(
        max_length=50,
        default='bi-bar-chart-line',
        verbose_name='Ícone Bootstrap',
        help_text='Classe do Bootstrap Icons (ex: bi-bar-chart-line)'
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem de Exibição'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Categoria de Painel'
        verbose_name_plural = 'Categorias de Painéis'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome

    @property
    def paineis_ativos(self):
        return self.paineis.filter(ativo=True)


class PainelBI(models.Model):
    """
    Painel Power BI a ser exibido via iframe.
    Cada painel pertence a uma categoria (menu lateral).
    Pode ser vinculado a um grupo específico para controle de acesso.
    """
    categoria = models.ForeignKey(
        CategoriaPainel,
        on_delete=models.CASCADE,
        related_name='paineis',
        verbose_name='Categoria'
    )
    grupo_acesso = models.ForeignKey(
        'auth.Group',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paineis_bi',
        verbose_name='Grupo de Acesso',
        help_text='Grupo que pode visualizar este painel. Vazio = visível para todos com acesso à categoria.'
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título do Painel'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Breve descrição do painel'
    )
    iframe_url = models.URLField(
        max_length=2000,
        blank=True,
        verbose_name='URL do iframe (Power BI)',
        help_text='Cole aqui a URL de incorporação do Power BI'
    )
    icone = models.CharField(
        max_length=50,
        default='bi-file-earmark-bar-graph',
        verbose_name='Ícone Bootstrap',
        help_text='Classe do Bootstrap Icons (ex: bi-file-earmark-bar-graph)'
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem de Exibição'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Painel BI'
        verbose_name_plural = 'Painéis BI'
        ordering = ['categoria__ordem', 'ordem', 'titulo']

    def __str__(self):
        grupo_str = f" [{self.grupo_acesso.name}]" if self.grupo_acesso else ""
        return f"{self.categoria.nome} - {self.titulo}{grupo_str}"

    @property
    def tem_iframe(self):
        return bool(self.iframe_url)
