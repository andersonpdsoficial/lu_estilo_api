from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import re
from app.models.client import Client as ClientModel
from app.models.user import User
from app.schemas.client import ClientCreate, Client
from app.database.database import get_db
from app.utils.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/clients", tags=["clients"])

def validate_cpf(cpf: str) -> bool:
    cpf = re.sub(r'[^\d]', '', cpf)
    return len(cpf) == 11 and cpf.isdigit()

def validate_phone(phone: str) -> bool:
    return bool(re.match(r'^\+?\d{10,15}$', phone))

@router.post("/", response_model=Client, summary="Criar cliente", description="Cria um novo cliente com email e CPF únicos")
def create_client(client: ClientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not validate_cpf(client.cpf):
        raise HTTPException(status_code=400, detail="Invalid CPF")
    if not validate_phone(client.phone):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    db_client = db.query(ClientModel).filter((ClientModel.email == client.email) | (ClientModel.cpf == client.cpf)).first()
    if db_client:
        raise HTTPException(status_code=400, detail="Email or CPF already registered")
    new_client = ClientModel(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@router.get("/", response_model=List[Client], summary="Listar clientes", description="Lista clientes com suporte a paginação e filtros")
def list_clients(
    skip: int = 0,
    limit: int = 10,
    name: str = None,
    email: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ClientModel)
    if name:
        query = query.filter(ClientModel.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(ClientModel.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/{id}", response_model=Client, summary="Obter cliente", description="Obtém detalhes de um cliente específico")
def get_client(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = db.query(ClientModel).filter(ClientModel.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{id}", response_model=Client, summary="Atualizar cliente", description="Atualiza os dados de um cliente")
def update_client(id: int, client: ClientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not validate_cpf(client.cpf):
        raise HTTPException(status_code=400, detail="Invalid CPF")
    if not validate_phone(client.phone):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    db_client = db.query(ClientModel).filter(ClientModel.id == id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db_client_check = db.query(ClientModel).filter(
        (ClientModel.email == client.email) | (ClientModel.cpf == client.cpf),
        ClientModel.id != id
    ).first()
    if db_client_check:
        raise HTTPException(status_code=400, detail="Email or CPF already registered")
    for key, value in client.dict().items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.delete("/{id}", summary="Deletar cliente", description="Remove um cliente (somente admin)")
def delete_client(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    client = db.query(ClientModel).filter(ClientModel.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"message": "Client deleted"}