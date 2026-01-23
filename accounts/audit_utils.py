"""
Utilitários para registro de logs de auditoria.
Funções helper para facilitar o registro de ações no sistema.
"""

from .models import AuditLog


def get_client_ip(request):
    """
    Obtém o endereço IP real do cliente, considerando proxies.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_action(user, action, description, request=None, severity='INFO', extra_data=None):
    """
    Registra uma ação de auditoria no sistema.
    
    Args:
        user: Objeto User do Django
        action: Tipo de ação (LOGIN, LOGOUT, VIEW, CREATE, UPDATE, DELETE, etc.)
        description: Descrição detalhada da ação
        request: Objeto HttpRequest (opcional)
        severity: Nível de severidade (INFO, WARNING, ERROR, CRITICAL)
        extra_data: Dicionário com dados adicionais (opcional)
    
    Returns:
        AuditLog: Objeto criado
    """
    log_data = {
        'user': user if user and user.is_authenticated else None,
        'username': user.username if user and user.is_authenticated else 'Anônimo',
        'action': action,
        'description': description,
        'severity': severity,
        'extra_data': extra_data,
    }
    
    # Adiciona informações da requisição se disponível
    if request:
        log_data.update({
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500],
            'path': request.path,
            'method': request.method,
        })
    
    return AuditLog.objects.create(**log_data)


def log_login(user, request, success=True):
    """Registra tentativa de login"""
    if success:
        description = f"Login realizado com sucesso"
        severity = 'INFO'
    else:
        description = f"Tentativa de login falhou"
        severity = 'WARNING'
    
    return log_action(
        user=user,
        action='LOGIN',
        description=description,
        request=request,
        severity=severity
    )


def log_logout(user, request):
    """Registra logout"""
    return log_action(
        user=user,
        action='LOGOUT',
        description=f"Logout realizado",
        request=request,
        severity='INFO'
    )


def log_view(user, request, page_name):
    """Registra visualização de página"""
    return log_action(
        user=user,
        action='VIEW',
        description=f"Acessou a página: {page_name}",
        request=request,
        severity='INFO'
    )


def log_access_denied(user, request, page_name):
    """Registra acesso negado"""
    return log_action(
        user=user,
        action='ACCESS_DENIED',
        description=f"Acesso negado à página: {page_name}",
        request=request,
        severity='WARNING'
    )


def log_create(user, request, object_type, object_name):
    """Registra criação de objeto"""
    return log_action(
        user=user,
        action='CREATE',
        description=f"Criou {object_type}: {object_name}",
        request=request,
        severity='INFO'
    )


def log_update(user, request, object_type, object_name):
    """Registra atualização de objeto"""
    return log_action(
        user=user,
        action='UPDATE',
        description=f"Atualizou {object_type}: {object_name}",
        request=request,
        severity='INFO'
    )


def log_delete(user, request, object_type, object_name):
    """Registra exclusão de objeto"""
    return log_action(
        user=user,
        action='DELETE',
        description=f"Excluiu {object_type}: {object_name}",
        request=request,
        severity='WARNING'
    )


def log_error(user, request, error_message):
    """Registra erro"""
    return log_action(
        user=user,
        action='ERROR',
        description=f"Erro: {error_message}",
        request=request,
        severity='ERROR'
    )
