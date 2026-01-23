from django.contrib import admin
from .models import AuditLog


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
