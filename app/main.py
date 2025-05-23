from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import sentry_sdk
from app.api import auth, clients, products, orders, whatsapp
from app.database.database import engine, Base

# Inicializar Sentry
sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)

app = FastAPI(
    title="Lu Estilo API",
    description="API para gerenciamento de clientes, produtos, pedidos e integração com WhatsApp",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar middleware do Sentry
app.add_middleware(SentryAsgiMiddleware)

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Incluir rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API da Lu Estilo!"}