# Plataforma de Alerta Colaborativo

O Plataforma Alerta Colaborativo é um sistema inteligente que transforma cidadãos em sensores humanos, permitindo o envio de alertas climáticos em tempo real.

A solução combina inteligência artificial e dados oficiais para validar relatos, gerar mapas dinâmicos de risco e apoiar respostas rápidas a eventos meteorológicos e hidrológicos.

[![Django CI](https://img.shields.io/badge/Django%20CI-passing-brightgreen)](https://github.com/fmartns/plataforma-alerta-colaborativo/actions)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-A%2B-blue)](https://github.com/fmartns/plataforma-alerta-colaborativo/actions)
[![Docker Build](https://img.shields.io/badge/Docker%20Build%20%26%20Push-passing-blue)](https://github.com/fmartns/plataforma-alerta-colaborativo/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Tecnologias

- **Backend**: Django 5.2, Django REST Framework  
- **Banco de Dados**: PostgreSQL (produção), SQLite (desenvolvimento)  
- **Infra**: Docker, Docker Compose  
- **Qualidade**: Black, Ruff, Flake8, Pyright  
- **CI/CD**: GitHub Actions (Testes, Lint, Docker Build)

## Como rodar

### 1. Clonar o repositório
```bash
git clone https://github.com/fmartns/plataforma-alerta-colaborativo.git
cd hub-backend
```

### 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
```

### 3. Rodar com Docker (recomendado)
```bash
docker compose up --build
```

A aplicação estará disponível em:
- API: http://127.0.0.1:8000  
- Admin: http://127.0.0.1:8000/admin/  
- Swagger: http://127.0.0.1:8000/swagger/  

### 4. Rodar localmente (sem Docker)
```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## Testes e Qualidade

Rodar os checadores de código e testes:
```bash
poetry run black .
poetry run ruff check . --fix
poetry run flake8 .
poetry run pyright
poetry run python manage.py test
```

## Docker

Build e execução manual:
```bash
docker build -t hub-backend -f docker/Dockerfile .
docker run --rm -p 8000:8000 --env-file .env hub-backend
```
