"""
Command para inicializar o banco de dados com usuários e grupos de exemplo.

Este comando cria:
- Grupo "Gestão" com acesso total (José e Caio)
- Grupo "Unidades" com acesso limitado (Rafael e Carlos)

Uso:
    python manage.py setup_users
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction


class Command(BaseCommand):
    help = 'Inicializa o banco de dados com usuários e grupos de exemplo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando configuração de usuários e grupos...'))
        
        try:
            with transaction.atomic():
                # Criar grupos
                grupo_gestao, created = Group.objects.get_or_create(name='Gestão')
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Grupo "Gestão" criado'))
                else:
                    self.stdout.write(self.style.WARNING(f'○ Grupo "Gestão" já existe'))
                
                grupo_unidades, created = Group.objects.get_or_create(name='Unidades')
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Grupo "Unidades" criado'))
                else:
                    self.stdout.write(self.style.WARNING(f'○ Grupo "Unidades" já existe'))
                
                self.stdout.write('')
                
                # Criar usuários do grupo Gestão
                usuarios_gestao = [
                    {
                        'username': 'jose',
                        'password': 'Jose@2025',
                        'first_name': 'José',
                        'last_name': 'Silva',
                        'email': 'jose@paineis.com',
                    },
                    {
                        'username': 'caio',
                        'password': 'Caio@2025',
                        'first_name': 'Caio',
                        'last_name': 'Santos',
                        'email': 'caio@paineis.com',
                    },
                ]
                
                for user_data in usuarios_gestao:
                    username = user_data['username']
                    if User.objects.filter(username=username).exists():
                        self.stdout.write(self.style.WARNING(f'○ Usuário "{username}" já existe'))
                        user = User.objects.get(username=username)
                    else:
                        user = User.objects.create_user(
                            username=user_data['username'],
                            password=user_data['password'],
                            first_name=user_data['first_name'],
                            last_name=user_data['last_name'],
                            email=user_data['email'],
                            is_active=True,
                        )
                        self.stdout.write(self.style.SUCCESS(
                            f'✓ Usuário "{username}" criado (senha: {user_data["password"]})'
                        ))
                    
                    # Adicionar ao grupo Gestão
                    if not user.groups.filter(name='Gestão').exists():
                        user.groups.add(grupo_gestao)
                        self.stdout.write(self.style.SUCCESS(f'  → Adicionado ao grupo "Gestão"'))
                
                self.stdout.write('')
                
                # Criar usuários do grupo Unidades
                usuarios_unidades = [
                    {
                        'username': 'rafael',
                        'password': 'Rafael@2025',
                        'first_name': 'Rafael',
                        'last_name': 'Oliveira',
                        'email': 'rafael@paineis.com',
                    },
                    {
                        'username': 'carlos',
                        'password': 'Carlos@2025',
                        'first_name': 'Carlos',
                        'last_name': 'Souza',
                        'email': 'carlos@paineis.com',
                    },
                ]
                
                for user_data in usuarios_unidades:
                    username = user_data['username']
                    if User.objects.filter(username=username).exists():
                        self.stdout.write(self.style.WARNING(f'○ Usuário "{username}" já existe'))
                        user = User.objects.get(username=username)
                    else:
                        user = User.objects.create_user(
                            username=user_data['username'],
                            password=user_data['password'],
                            first_name=user_data['first_name'],
                            last_name=user_data['last_name'],
                            email=user_data['email'],
                            is_active=True,
                        )
                        self.stdout.write(self.style.SUCCESS(
                            f'✓ Usuário "{username}" criado (senha: {user_data["password"]})'
                        ))
                    
                    # Adicionar ao grupo Unidades
                    if not user.groups.filter(name='Unidades').exists():
                        user.groups.add(grupo_unidades)
                        self.stdout.write(self.style.SUCCESS(f'  → Adicionado ao grupo "Unidades"'))
                
                self.stdout.write('')
                self.stdout.write(self.style.SUCCESS('='*60))
                self.stdout.write(self.style.SUCCESS('CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!'))
                self.stdout.write(self.style.SUCCESS('='*60))
                self.stdout.write('')
                self.stdout.write('Usuários criados:')
                self.stdout.write('')
                self.stdout.write(self.style.SUCCESS('Grupo GESTÃO (Acesso Total):'))
                self.stdout.write('  • Usuário: jose    | Senha: Jose@2025')
                self.stdout.write('  • Usuário: caio    | Senha: Caio@2025')
                self.stdout.write('')
                self.stdout.write(self.style.SUCCESS('Grupo UNIDADES (Acesso Limitado):'))
                self.stdout.write('  • Usuário: rafael  | Senha: Rafael@2025')
                self.stdout.write('  • Usuário: carlos  | Senha: Carlos@2025')
                self.stdout.write('')
                self.stdout.write(self.style.WARNING('IMPORTANTE: Altere as senhas após o primeiro acesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao configurar usuários: {str(e)}'))
            raise
