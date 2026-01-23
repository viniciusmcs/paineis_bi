from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core.paginator import Paginator
from .decorators import gestao_required
from .models import AuditLog
from .audit_utils import log_login, log_logout, log_view, log_access_denied


@sensitive_post_parameters('password')
@csrf_protect
@never_cache
def login_view(request):
    """
    View de login com proteções de segurança:
    - @sensitive_post_parameters: Impede que a senha apareça em logs de erro
    - @csrf_protect: Proteção contra CSRF attacks
    - @never_cache: Impede cache da página de login
    """
    if request.user.is_authenticated:
        return redirect('accounts:home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Validação básica
        if not username or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'accounts/login.html')
        
        # Autenticação - Django já protege contra SQL injection
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                log_login(user, request, success=True)
                messages.success(request, f'Bem-vindo, {user.get_full_name() or user.username}!')
                
                # Redireciona para a próxima página ou home
                next_url = request.GET.get('next', 'accounts:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Sua conta está inativa. Entre em contato com o administrador.')
        else:
            # Log de tentativa de login falha
            if username:
                from django.contrib.auth.models import User
                try:
                    failed_user = User.objects.get(username=username)
                    log_login(failed_user, request, success=False)
                except User.DoesNotExist:
                    pass
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """
    View de logout - apenas usuários autenticados podem fazer logout
    """
    log_logout(request.user, request)
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('accounts:login')


@login_required
def home_view(request):
    """
    Página inicial do sistema - requer autenticação
    """
    log_view(request.user, request, 'Home')
    
    user = request.user
    
    # Obtém os grupos do usuário
    grupos = user.groups.all()
    
    # Verifica se o usuário pertence ao grupo Gestão (acesso total)
    is_gestao = user.groups.filter(name='Gestão').exists()
    
    context = {
        'user': user,
        'grupos': grupos,
        'is_gestao': is_gestao,
    }
    
    return render(request, 'accounts/home.html', context)


@gestao_required
def gestao_dashboard(request):
    """
    Dashboard exclusivo para o grupo Gestão
    Exemplo de uso do decorator @gestao_required
    """
    log_view(request.user, request, 'Dashboard de Gestão')
    
    context = {
        'titulo': 'Dashboard de Gestão',
        'descricao': 'Esta página é acessível apenas para usuários do grupo Gestão.',
    }
    return render(request, 'accounts/gestao_dashboard.html', context)


@gestao_required
def audit_logs_view(request):
    """
    View para visualizar logs de auditoria
    Apenas usuários do grupo Gestão têm acesso
    """
    log_view(request.user, request, 'Logs de Auditoria')
    
    # Filtros
    action_filter = request.GET.get('action', '')
    user_filter = request.GET.get('user', '')
    date_filter = request.GET.get('date', '')
    
    # Query base
    logs = AuditLog.objects.select_related('user').all()
    
    # Aplicar filtros
    if action_filter:
        logs = logs.filter(action=action_filter)
    if user_filter:
        logs = logs.filter(username__icontains=user_filter)
    if date_filter:
        from datetime import datetime
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            logs = logs.filter(timestamp__date=date_obj)
        except ValueError:
            pass
    
    # Paginação
    paginator = Paginator(logs, 50)  # 50 logs por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total_logs = logs.count()
    total_logins = AuditLog.objects.filter(action='LOGIN').count()
    total_access_denied = AuditLog.objects.filter(action='ACCESS_DENIED').count()
    
    context = {
        'page_obj': page_obj,
        'total_logs': total_logs,
        'total_logins': total_logins,
        'total_access_denied': total_access_denied,
        'action_filter': action_filter,
        'user_filter': user_filter,
        'date_filter': date_filter,
        'action_choices': AuditLog.ACTION_CHOICES,
    }
    
    return render(request, 'accounts/audit_logs.html', context)
