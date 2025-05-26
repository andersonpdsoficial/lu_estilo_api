#  Lu Estilo API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

## 📋 Sobre o Projeto

API RESTful desenvolvida em FastAPI para o sistema de gestão da Lu Estilo, oferecendo funcionalidades completas para gerenciamento de clientes, produtos, pedidos e integração com WhatsApp.

## ✨ Funcionalidades

- 🔐 **Autenticação JWT**
  - Registro e login de usuários
  - Roles: admin e usuário comum
  - Refresh token

- 👥 **Gestão de Clientes**
  - CRUD completo
  - Validação de CPF
  - Histórico de pedidos

- 📦 **Gestão de Produtos**
  - Controle de estoque
  - Upload de imagens
  - Categorização

- 🧾 **Pedidos**
  - Fluxo completo (criação à entrega)
  - Status em tempo real
  - Histórico detalhado

- 📲 **Integração WhatsApp**
  - Notificações automáticas
  - Status de entrega
  - Comunicação com clientes

## 🛠️ Tecnologias

- **Backend**: FastAPI
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrações**: Alembic
- **Autenticação**: JWT
- **Containerização**: Docker
- **Testes**: Pytest
- **Monitoramento**: Sentry

## 🚀 Começando

### Pré-requisitos

- Python 3.11+
- PostgreSQL 13+
- Docker e Docker Compose
- Git

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/andersonpdsoficial/lu_estilo_api
cd lu_estilo_api
```

2. **Configure o ambiente virtual**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
# Windows
copy .env.example .env
# Linux/Mac
cp .env.example .env
```

5. **Configure o arquivo .env**
```env
DATABASE_URL=postgresql://postgres:123456@db:5432/lu_estilo
JWT_SECRET_KEY=sua-chave-secreta-jwt-aqui
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
WHATSAPP_API_TOKEN=seu-token-whatsapp-aqui
WHATSAPP_PHONE_NUMBER_ID=seu-id-telefone-whatsapp
SENTRY_DSN=
```

### 🐳 Executando com Docker

1. **Inicie os containers**
```bash
docker-compose up -d
```

2. **Aplique as migrações**
```bash
docker-compose run --rm app alembic upgrade head
```

3. **Acesse a API**
```
http://localhost:8000/docs
```

### 🧪 Executando os Testes

```bash
# Criar banco de testes
psql -U postgres -c "CREATE DATABASE lu_estilo_test;"

# Executar testes
pytest app/tests
```

## 📁 Estrutura do Projeto

```
lu_estilo_api/
├── app/
│   ├── alembic/          # Migrações do banco
│   ├── api/              # Endpoints da API
│   ├── database/         # Configuração do banco
│   ├── models/           # Modelos SQLAlchemy
│   ├── schemas/          # Schemas Pydantic
│   ├── tests/            # Testes automatizados
│   ├── utils/            # Utilitários
│   └── main.py           # Ponto de entrada
├── alembic.ini           # Configuração Alembic
├── .env                  # Variáveis de ambiente
├── Dockerfile           # Configuração Docker
├── docker-compose.yml   # Orquestração containers
└── requirements.txt     # Dependências Python
```

## 📡 Endpoints Principais

![Captura de tela 2025-05-26 104747](https://github.com/user-attachments/assets/b93f28e8-8389-4583-877b-e243c11d1df0)
![Captura de tela 2025-05-26 104740](https://github.com/user-attachments/assets/54e1df6e-724b-4371-8690-cd5cd4f51553)
![Captura de tela 2025-05-26 104755](https://github.com/user-attachments/assets/600005ad-4191-4f3d-91c8-122bc896b737)
![Captura de tela 2025-05-26 104802](https://github.com/user-attachments/assets/7cdd5283-b43d-4603-a03e-aec02c24415e)

### 🔐 Autenticação
- `POST /auth/register` - Registro de usuário
- `POST /auth/login` - Login e obtenção do token
- `POST /auth/refresh` - Renovação do token

### 👥 Clientes
- `POST /clients` - Criar cliente (admin)
- `GET /clients` - Listar todos (admin)
- `GET /clients/{id}` - Ver um cliente
- `PUT /clients/{id}` - Atualizar (admin)
- `DELETE /clients/{id}` - Deletar (admin)

### 📦 Produtos
- `POST /products` - Criar produto (admin)
- `GET /products` - Listar todos
- `GET /products/{id}` - Ver produto
- `PUT /products/{id}` - Atualizar (admin)
- `DELETE /products/{id}` - Deletar (admin)

### 🧾 Pedidos
- `POST /orders` - Criar pedido
- `GET /orders` - Listar pedidos
- `GET /orders/{id}` - Ver detalhes
- `PUT /orders/{id}` - Atualizar status (admin)

### 📲 WhatsApp
- `POST /whatsapp/send` - Enviar mensagem (admin)

## 🛠️ Solução de Problemas

### Banco não conecta?
1. Verifique a `DATABASE_URL` no `.env`
2. Confirme se o PostgreSQL está rodando
3. Teste a conexão:
```bash
python test_db.py
```

### Erro de codificação no .env?
1. Salve o arquivo em UTF-8
2. Evite caracteres especiais na senha
3. Verifique com:
```powershell
Get-Content .env -Raw
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

