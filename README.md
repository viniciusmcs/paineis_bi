# paineis_bi

Sistema Django para autenticação, controle de acesso por grupos e visualização de painéis BI.

## Requisitos

- Python 3.12+
- Pip
- Docker (opcional, para execução em container)

## Execução local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Aplicação disponível em `http://localhost:8000`.

## Execução com Docker (porta 8002)

Build da imagem:

```bash
docker build -t paineis_bi .
```

Execução do container na porta 8002:

```bash
docker run -d --name paineis_bi -p 8002:8002 \
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,10.0.125.4 \
  paineis_bi
```

Aplicação disponível em `http://10.0.125.4:8002`.

## Variáveis de ambiente

- `DJANGO_SECRET_KEY` (opcional)
- `DJANGO_DEBUG` (`True` ou `False`)
- `DJANGO_ALLOWED_HOSTS` (lista separada por vírgula)

## Comandos úteis

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```
