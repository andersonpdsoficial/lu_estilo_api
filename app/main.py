from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import sentry_sdk
from app.api import auth, clients, products, orders, whatsapp
from app.database.database import engine, Base
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Sentry apenas se SENTRY_DSN estiver configurado e válido
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn and sentry_dsn.strip() and sentry_dsn.startswith("https://"):
    try:
        sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=1.0,
        )
    except Exception as e:
        print(f"Sentry initialization skipped: {str(e)}")

app = FastAPI(
    title="Lu Estilo API",
    description="API para gerenciamento de clientes, produtos, pedidos e integração com WhatsApp para a Lu Estilo.",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar middleware do Sentry apenas se inicializado
if sentry_dsn and sentry_dsn.strip() and sentry_dsn.startswith("https://"):
    app.add_middleware(SentryAsgiMiddleware)

# Criar tabelas no banco
# Base.metadata.create_all(bind=engine)

# Incluir rotas
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(whatsapp.router)

@app.get("/")
async def root():
    return {"message": "Hello, Lu Estilo!"}