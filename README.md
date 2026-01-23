# Painéis BI - Sistema de Business Intelligence

Sistema de autenticação e controle de acesso baseado em grupos para gestão de painéis de Business Intelligence.

## 🚀 Início Rápido

### 1. Iniciar o servidor Django
```bash
python manage.py runserver
```

### 2. Acessar o sistema
Abra seu navegador e acesse: **http://localhost:8000/**

### 3. Fazer login
Use um dos usuários de exemplo:

#### 👥 Grupo Gestão (Acesso Total)
- **Usuário**: `jose` | **Senha**: `Jose@2025`
- **Usuário**: `caio` | **Senha**: `Caio@2025`

#### 👤 Grupo Unidades (Acesso Limitado)
- **Usuário**: `rafael` | **Senha**: `Rafael@2025`
- **Usuário**: `carlos` | **Senha**: `Carlos@2025`

## 📁 Estrutura do Projeto

```
paineis_bi/
├── accounts/                      # App de autenticação
│   ├── decorators.py             # Decoradores de controle de acesso
│   ├── views.py                  # Views de login, logout e home
│   ├── urls.py                   # Rotas do app
│   └── management/               # Comandos personalizados
│       └── commands/
│           └── setup_users.py    # Comando para criar usuários
├── templates/                     # Templates HTML
│   ├── base.html                 # Template base
│   └── accounts/
│       ├── login.html            # Tela de login
│       ├── home.html             # Página inicial
│       └── gestao_dashboard.html # Dashboard da gestão
├── paineis_bi/                   # Configurações do projeto
│   ├── settings.py              # Configurações (com medidas de segurança)
│   └── urls.py                  # URLs principais
├── SEGURANCA.md                  # Documentação de segurança
└── README.md                     # Este arquivo
```

## 🔐 Funcionalidades de Segurança

✅ **Proteção contra SQL Injection** - Django ORM com prepared statements  
✅ **Proteção CSRF** - Token CSRF em todos os formulários  
✅ **Proteção XSS** - Auto-escape de templates  
✅ **Proteção Clickjacking** - X-Frame-Options configurado  
✅ **Sessões Seguras** - Cookies HttpOnly, timeout de 30 minutos  
✅ **Hashing de Senhas** - PBKDF2 com SHA256  
✅ **Controle de Acesso** - Sistema de grupos e permissões  
✅ **Validação de Entrada** - Sanitização de todos os inputs  

Para mais detalhes, consulte: [SEGURANCA.md](SEGURANCA.md)

## 🎯 Controle de Acesso por Grupos

### Grupo Gestão
- Acesso total ao sistema
- Pode visualizar todos os relatórios
- Pode acessar configurações avançadas
- Pode gerenciar usuários

### Grupo Unidades
- Acesso limitado
- Permissões definidas por módulo
- Não pode acessar áreas administrativas

## 🛠️ Comandos Úteis

### Recriar usuários de exemplo
```bash
python manage.py setup_users
```

### Criar um superusuário (admin)
```bash
python manage.py createsuperuser
```

### Aplicar migrações
```bash
python manage.py migrate
```

### Acessar o admin do Django
http://localhost:8000/admin/

## 💻 Como Usar os Decoradores de Controle de Acesso

### 1. Exigir autenticação
```python
from django.contrib.auth.decorators import login_required

@login_required
def minha_view(request):
    return render(request, 'template.html')
```

### 2. Exigir grupo específico
```python
from accounts.decorators import group_required

@group_required('Gestão')
def view_exclusiva_gestao(request):
    return render(request, 'template.html')
```

### 3. Exigir um de vários grupos
```python
from accounts.decorators import group_required

@group_required('Gestão', 'Unidades')
def view_multiplos_grupos(request):
    return render(request, 'template.html')
```

### 4. Usar decoradores simplificados
```python
from accounts.decorators import gestao_required, unidades_required

@gestao_required
def view_gestao(request):
    return render(request, 'template.html')

@unidades_required
def view_unidades(request):
    return render(request, 'template.html')
```

## 🎨 Interface

- **Design Moderno**: Bootstrap 5 com gradientes e animações
- **Responsivo**: Funciona em desktop, tablet e mobile
- **Ícones**: Bootstrap Icons integrados
- **Mensagens**: Sistema de feedback visual para o usuário
- **Acessibilidade**: Seguindo padrões WCAG

## 📱 Páginas Disponíveis

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/` | Página inicial | Requer login |
| `/login/` | Tela de login | Público |
| `/logout/` | Encerrar sessão | Usuários autenticados |
| `/gestao/dashboard/` | Dashboard de gestão | Apenas grupo Gestão |
| `/admin/` | Painel administrativo | Superusuários |

## 🔄 Próximas Funcionalidades

- [ ] Recuperação de senha
- [ ] Autenticação de dois fatores (2FA)
- [ ] Log de auditoria
- [ ] Rate limiting no login
- [ ] Módulos específicos com permissões granulares
- [ ] Perfil de usuário editável
- [ ] Histórico de acessos
- [ ] Dashboard com gráficos e métricas

## 📝 Notas Importantes

### Segurança em Produção
Antes de colocar em produção, configure:
- `DEBUG = False`
- `ALLOWED_HOSTS` com seu domínio
- `SECRET_KEY` com uma chave aleatória segura
- Habilite HTTPS e configure cookies seguros
- Configure banco de dados de produção (PostgreSQL, MySQL)
- Configure servidor de arquivos estáticos

### Alteração de Senhas
**IMPORTANTE**: Altere as senhas padrão após o primeiro acesso!

### Backup
Faça backup regular do banco de dados:
```bash
python manage.py dumpdata > backup.json
```

Restaurar backup:
```bash
python manage.py loaddata backup.json
```

## 🐛 Solução de Problemas

### Erro ao iniciar o servidor
```bash
# Verifique se o ambiente virtual está ativado
.\.venv\Scripts\activate

# Instale as dependências
pip install django
```

### Usuários não foram criados
```bash
python manage.py setup_users
```

### Problemas com migrações
```bash
python manage.py migrate --run-syncdb
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação em `SEGURANCA.md`
2. Verifique os logs do Django
3. Entre em contato com o administrador do sistema

## 📄 Licença

Este projeto é um sistema interno de BI. Todos os direitos reservados.

---

**Desenvolvido com ❤️ usando Django 6.0 e Bootstrap 5**
