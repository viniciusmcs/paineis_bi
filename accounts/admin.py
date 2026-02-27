from django.contrib import admin
from .models import AuditLog, CategoriaPainel, PainelBI


class PainelBIInline(admin.TabularInline):
    """Inline para gerenciar painéis dentro da categoria"""
    model = PainelBI
    extra = 1
    fields = ['titulo', 'grupo_acesso', 'iframe_url', 'icone', 'ordem', 'ativo']
    ordering = ['ordem', 'titulo']


@admin.register(CategoriaPainel)
class CategoriaPainelAdmin(admin.ModelAdmin):
    """Admin para gerenciar categorias de painéis (menus laterais)"""
    list_display = ['nome', 'icone', 'ordem', 'ativo', 'total_paineis', 'criado_em']
    list_filter = ['ativo']
    list_editable = ['ordem', 'ativo']
    search_fields = ['nome']
    ordering = ['ordem', 'nome']
    inlines = [PainelBIInline]

    def total_paineis(self, obj):
        return obj.paineis.count()
    total_paineis.short_description = 'Nº Painéis'


@admin.register(PainelBI)
class PainelBIAdmin(admin.ModelAdmin):
    """Admin para gerenciar painéis Power BI individuais"""
    list_display = ['titulo', 'categoria', 'grupo_acesso', 'tem_iframe_display', 'ordem', 'ativo', 'atualizado_em']
    list_filter = ['categoria', 'grupo_acesso', 'ativo']
    list_editable = ['ordem', 'ativo']
    search_fields = ['titulo', 'descricao', 'grupo_acesso__name']
    ordering = ['categoria__ordem', 'ordem', 'titulo']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('categoria', 'titulo', 'descricao', 'icone')
        }),
        ('Controle de Acesso', {
            'fields': ('grupo_acesso',),
            'description': 'Selecione o grupo que terá acesso a este painel. O grupo Gestão sempre tem acesso a todos.'
        }),
        ('Power BI', {
            'fields': ('iframe_url',),
            'description': 'Cole a URL de incorporação do Power BI. Obtenha em: Arquivo > Inserir relatório > Site ou portal'
        }),
        ('Configurações', {
            'fields': ('ordem', 'ativo')
        }),
    )

    def tem_iframe_display(self, obj):
        return '✅' if obj.tem_iframe else '❌'
    tem_iframe_display.short_description = 'iframe configurado'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Configuração do admin para visualização dos logs de auditoria
    """
    list_display = ['timestamp', 'username', 'action', 'description', 'ip_address', 'severity']
    list_filter = ['action', 'severity', 'timestamp']
    search_fields = ['username', 'description', 'ip_address']
    readonly_fields = ['user', 'username', 'action', 'description', 'severity', 
                      'ip_address', 'user_agent', 'path', 'method', 'extra_data', 'timestamp']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        """Não permite adicionar logs manualmente"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Apenas superusuários podem deletar logs"""
        return request.user.is_superuser
