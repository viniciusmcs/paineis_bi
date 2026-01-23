# Sistema de Autenticação - Painéis BI

## 🔐 Medidas de Segurança Implementadas

### 1. Proteção contra SQL Injection
- **Django ORM**: Todas as consultas ao banco utilizam o ORM do Django, que automaticamente escapa e sanitiza os parâmetros
- **Prepared Statements**: O ORM utiliza prepared statements internamente
- **Validação de Entrada**: Validação de dados antes de processamento

### 2. Proteção CSRF (Cross-Site Request Forgery)
- **Middleware CSRF**: Habilitado globalmente em `settings.py`
- **Token CSRF**: Todos os formulários incluem `{% csrf_token %}`
- **Cookie CSRF**: Configurado com `HttpOnly` e `SameSite=Lax`
- **Decorator @csrf_protect**: Aplicado nas views sensíveis

### 3. Proteção de Sessão
- **Session Hijacking**: Cookies de sessão com `HttpOnly=True`
- **Timeout de Sessão**: Sessão expira após 30 minutos de inatividade
- **SESSION_SAVE_EVERY_REQUEST**: Renovação automática do timeout
- **SameSite Cookie**: Configurado como 'Lax' para prevenir CSRF

### 4. Proteção de Senha
- **Hashing Seguro**: Django usa PBKDF2 com SHA256 por padrão
- **Password Validators**: Validação de força da senha (similaridade, comprimento mínimo, senhas comuns, só números)
- **@sensitive_post_parameters**: Impede que senhas apareçam em logs de erro
- **Autocomplete**: Configurado corretamente nos campos de senha

### 5. Proteção XSS (Cross-Site Scripting)
- **Auto-escape de Templates**: Django escapa automaticamente variáveis nos templates
- **SECURE_BROWSER_XSS_FILTER**: Habilitado para ativar filtro XSS do navegador
- **Content Security**: Validação de entrada do usuário

### 6. Proteção Clickjacking
- **X-Frame-Options**: Configurado como 'DENY' para prevenir iframe embedding
- **Middleware Clickjacking**: Habilitado globalmente

### 7. Autenticação Segura
- **@login_required**: Decorator para proteger views que requerem autenticação
- **is_authenticated**: Verificação de autenticação antes de operações sensíveis
- **Redirect Seguro**: Validação da URL de redirecionamento após login
- **Mensagens de Erro Genéricas**: Não revela se usuário existe ou não

### 8. Controle de Acesso Baseado em Grupos
- **Sistema de Grupos**: Django Groups para segregação de permissões
- **Grupo "Gestão"**: Acesso total ao sistema
- **Grupo "Unidades"**: Acesso limitado conforme módulos
- **Verificação de Permissões**: Validação em cada view

### 9. Outras Medidas
- **@never_cache**: Impede cache de páginas sensíveis (login)
- **Input Validation**: Validação de comprimento máximo nos campos
- **Trim de Strings**: Remoção de espaços em branco nos inputs
- **novalidate**: Desabilita validação HTML5 para usar validação do servidor
- **maxlength**: Limite de caracteres nos campos de entrada

## 📋 Usuários de Exemplo

### Grupo Gestão (Acesso Total)
- **Usuário**: jose | **Senha**: Jose@2025
- **Usuário**: caio | **Senha**: Caio@2025

### Grupo Unidades (Acesso Limitado)
- **Usuário**: rafael | **Senha**: Rafael@2025
- **Usuário**: carlos | **Senha**: Carlos@2025

## 🚀 Como Usar

### 1. Iniciar o servidor
```bash
python manage.py runserver
```

### 2. Acessar o sistema
Navegue para: http://localhost:8000/

### 3. Fazer login
Use um dos usuários de exemplo acima

### 4. Explorar funcionalidades
- **Home**: Visualiza informações do usuário e grupos
- **Logout**: Encerra a sessão de forma segura

## ⚙️ Configurações Adicionais para Produção

Quando for para produção, altere estas configurações em `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']
SECRET_KEY = 'gere-uma-chave-secreta-aleatoria'

# Habilitar HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## 🔄 Recriar Usuários

Se precisar recriar os usuários de exemplo:
```bash
python manage.py setup_users
```

## 📝 Próximos Passos

1. Implementar recuperação de senha
2. Adicionar autenticação de dois fatores (2FA)
3. Implementar log de auditoria
4. Adicionar rate limiting no login
5. Implementar módulos específicos com permissões granulares
6. Adicionar testes automatizados de segurança
7. Configurar SSL/TLS em produção
8. Implementar CAPTCHA após múltiplas tentativas

## 🛡️ Manutenção de Segurança

- Mantenha o Django sempre atualizado
- Revise logs de acesso regularmente
- Monitore tentativas de login falhas
- Implemente política de troca periódica de senhas
- Realize auditorias de segurança periódicas
- Configure backup automático do banco de dados
