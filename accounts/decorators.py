"""
Decoradores personalizados para controle de acesso baseado em grupos.

Exemplo de uso:

@group_required('Gestão')
def minha_view(request):
    # Código da view
    pass

@group_required(['Gestão', 'Unidades'])
def outra_view(request):
    # Código da view
    pass
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def group_required(*group_names):
    """
    Decorator para verificar se o usuário pertence a um ou mais grupos.
    
    Args:
        *group_names: Nome(s) do(s) grupo(s) permitidos
    
    Uso:
        @group_required('Gestão')
        @group_required('Gestão', 'Unidades')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Converte para lista se for string única
            groups = group_names if isinstance(group_names, (list, tuple)) else [group_names]
            
            # Verifica se o usuário é superuser (acesso total)
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verifica se o usuário pertence a algum dos grupos
            user_groups = request.user.groups.values_list('name', flat=True)
            
            if any(group in user_groups for group in groups):
                return view_func(request, *args, **kwargs)
            
            # Registra acesso negado
            from .audit_utils import log_access_denied
            log_access_denied(request.user, request, request.path)
            
            # Usuário não tem permissão
            messages.error(
                request,
                f'Você não tem permissão para acessar esta página. '
                f'Grupos necessários: {", ".join(groups)}'
            )
            return redirect('accounts:home')
        
        return wrapper
    return decorator


def gestao_required(view_func):
    """
    Decorator simplificado para views que requerem grupo Gestão.
    
    Uso:
        @gestao_required
        def minha_view(request):
            pass
    """
    return group_required('Gestão')(view_func)


def unidades_required(view_func):
    """
    Decorator simplificado para views que requerem grupo Unidades.
    
    Uso:
        @unidades_required
        def minha_view(request):
            pass
    """
    return group_required('Unidades')(view_func)
