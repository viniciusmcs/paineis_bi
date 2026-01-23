# 🧪 Guia de Testes - Sistema de Login

## Iniciando o Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: **http://localhost:8000/**

---

## 🎯 Testes de Funcionalidade

### ✅ Teste 1: Acesso Sem Autenticação
1. Acesse http://localhost:8000/
2. **Esperado**: Deve redirecionar automaticamente para `/login/`
3. ✓ Sistema protege rotas que requerem autenticação

### ✅ Teste 2: Login - Usuário Gestão
1. Acesse http://localhost:8000/login/
2. Digite:
   - **Usuário**: `jose`
   - **Senha**: `Jose@2025`
3. Clique em "Entrar"
4. **Esperado**: 
   - Mensagem "Bem-vindo, José Silva!"
   - Redirecionamento para a home
   - Badge "Gestão" visível
   - Dashboard de Gestão disponível nos módulos

### ✅ Teste 3: Login - Usuário Unidades
1. Faça logout (menu superior direito)
2. Faça login com:
   - **Usuário**: `rafael`
   - **Senha**: `Rafael@2025`
3. **Esperado**:
   - Badge "Unidades" visível
   - Mensagem de acesso limitado
   - Módulos limitados

### ✅ Teste 4: Proteção de Rota - Dashboard Gestão
1. Estando logado como `rafael` (grupo Unidades)
2. Tente acessar: http://localhost:8000/gestao/dashboard/
3. **Esperado**:
   - Mensagem de erro: "Você não tem permissão..."
   - Redirecionamento para home
   - ✓ Controle de acesso funcionando

### ✅ Teste 5: Acesso Autorizado - Dashboard Gestão
1. Faça logout
2. Faça login como `jose` (grupo Gestão)
3. Clique no card "Dashboard Gestão" na home
4. **Esperado**:
   - Acesso permitido
   - Página com badge "Acesso Autorizado"
   - Funcionalidades exclusivas exibidas

### ✅ Teste 6: Proteção CSRF
1. Abra as ferramentas de desenvolvedor (F12)
2. Vá para a aba "Network" (Rede)
3. Faça logout e vá para o login
4. Observe a requisição POST ao fazer login
5. **Esperado**:
   - Token CSRF presente no formulário
   - Cookie `csrftoken` presente
   - ✓ Proteção CSRF ativa

### ✅ Teste 7: Timeout de Sessão
1. Faça login normalmente
2. Aguarde 31 minutos sem atividade
3. Tente navegar para qualquer página
4. **Esperado**:
   - Sessão expirada
   - Redirecionamento para login
   - ✓ Timeout funcionando (configurado para 30 minutos)

### ✅ Teste 8: Tentativa de Login Inválido
1. Acesse /login/
2. Digite credenciais incorretas:
   - **Usuário**: `usuario_invalido`
   - **Senha**: `senha_errada`
3. **Esperado**:
   - Mensagem: "Usuário ou senha inválidos"
   - Permanece na tela de login
   - ✓ Não revela se o usuário existe

### ✅ Teste 9: Campos Vazios
1. Acesse /login/
2. Deixe os campos em branco
3. Clique em "Entrar"
4. **Esperado**:
   - Mensagem: "Por favor, preencha todos os campos"
   - Validação do lado do servidor funcionando

### ✅ Teste 10: Navegação Autenticada
1. Faça login como `caio`
2. Observe a navbar superior
3. **Esperado**:
   - Nome completo no menu: "Caio Santos"
   - Badge do grupo "Gestão"
   - Link de logout disponível
   - ✓ Interface mostrando informações do usuário

---

## 🔒 Testes de Segurança

### 🛡️ Proteção SQL Injection
**Teste Manual**:
1. Tente fazer login com:
   - **Usuário**: `admin' OR '1'='1`
   - **Senha**: `qualquer`
2. **Esperado**: Login falha - Django ORM protege contra SQL injection

### 🛡️ Proteção XSS
**Teste Manual**:
1. Crie um superusuário: `python manage.py createsuperuser`
2. Acesse http://localhost:8000/admin/
3. Crie um usuário com nome: `<script>alert('XSS')</script>`
4. Faça login com esse usuário
5. **Esperado**: Script não é executado - Django escapa HTML automaticamente

### 🛡️ Proteção Clickjacking
**Teste com DevTools**:
1. Abra as ferramentas de desenvolvedor
2. Vá para "Network" (Rede)
3. Carregue a página de login
4. Observe os headers da resposta
5. **Esperado**: Header `X-Frame-Options: DENY` presente

---

## 📊 Checklist de Verificação

- [ ] Sistema redireciona para login quando não autenticado
- [ ] Login funciona com credenciais corretas
- [ ] Login falha com credenciais incorretas
- [ ] Mensagens de erro/sucesso são exibidas
- [ ] Grupos são exibidos corretamente
- [ ] Dashboard de Gestão acessível apenas para grupo Gestão
- [ ] Controle de acesso bloqueia usuários sem permissão
- [ ] Logout funciona e limpa a sessão
- [ ] Interface é responsiva (teste em mobile)
- [ ] Timeout de sessão funciona (30 minutos)
- [ ] Token CSRF presente em formulários
- [ ] Cookies com flags de segurança configurados
- [ ] Senhas não aparecem em logs
- [ ] Navegação funciona corretamente

---

## 🐛 Debug - Comandos Úteis

### Ver usuários e grupos
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group

# Listar usuários
for user in User.objects.all():
    print(f"{user.username} - Grupos: {[g.name for g in user.groups.all()]}")

# Listar grupos
for group in Group.objects.all():
    print(f"Grupo: {group.name} - Usuários: {group.user_set.count()}")
```

### Resetar senha de um usuário
```python
from django.contrib.auth.models import User

user = User.objects.get(username='jose')
user.set_password('NovaSenha@2025')
user.save()
```

### Verificar permissões
```python
user = User.objects.get(username='jose')
print(f"Grupos: {[g.name for g in user.groups.all()]}")
print(f"É Gestão: {user.groups.filter(name='Gestão').exists()}")
```

---

## ✨ Testes Visuais

### Interface do Login
- [ ] Gradiente de fundo atraente
- [ ] Card centralizado e responsivo
- [ ] Ícones visíveis nos campos
- [ ] Botão com hover effect
- [ ] Mensagens de alerta bem visíveis

### Interface da Home
- [ ] Welcome card destacado
- [ ] Cards de informação bem organizados
- [ ] Badges de grupos coloridos
- [ ] Cards de módulos clicáveis (para Gestão)
- [ ] Footer sempre no final da página

### Interface da Navbar
- [ ] Logo e nome do sistema visíveis
- [ ] Menu dropdown do usuário funcionando
- [ ] Badge do grupo exibido no dropdown
- [ ] Botão de logout acessível

---

## 📈 Próximos Testes (Após Implementação)

- [ ] Rate limiting (limitar tentativas de login)
- [ ] Captcha após N tentativas
- [ ] Log de auditoria
- [ ] 2FA (autenticação de dois fatores)
- [ ] Recuperação de senha
- [ ] Alteração de senha
- [ ] Histórico de logins

---

## 🎓 Dicas para Testes

1. **Use diferentes navegadores**: Chrome, Firefox, Edge
2. **Teste em diferentes tamanhos de tela**: Desktop, tablet, mobile
3. **Limpe o cache** entre testes para evitar problemas
4. **Use modo anônimo** para testar como novo usuário
5. **Verifique o console** do navegador para erros JavaScript

---

## 📝 Relatando Problemas

Se encontrar algum problema:
1. Anote o que estava fazendo
2. Copie a mensagem de erro (se houver)
3. Verifique o terminal onde o servidor está rodando
4. Tire um screenshot se necessário

---

**Última atualização**: 23 de janeiro de 2026
