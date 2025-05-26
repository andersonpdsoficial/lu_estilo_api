from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.product import Product
from app.schemas.product import ProductCreate, Product
from app.database.database import get_db
from app.utils.auth import get_current_user, get_current_admin
from app.models.user import User
import re

router = APIRouter(prefix="/products", tags=["products"])

def validate_barcode(barcode: str) -> bool:
    return bool(re.match(r'^\d{8,13}$', barcode))

@router.post("/", response_model=Product, summary="Criar produto", description="Cria um novo produto com atributos específicos")
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not validate_barcode(product.barcode):
        raise HTTPException(status_code=400, detail="Invalid barcode")
    db_product = db.query(Product).filter(Product.barcode == product.barcode).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Barcode already registered")
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[Product], summary="Listar produtos", description="Lista produtos com filtros de categoria, preço e disponibilidade")
def list_products(
    skip: int = 0,
    limit: int = 10,
    section: str = None,
    min_price: float = None,
    max_price: float = None,
    available: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product)
    if section:
        query = query.filter(Product.section == section)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if available is not None:
        query = query.filter(Product.stock > 0 if available else Product.stock == 0)
    return query.offset(skip).limit(limit).all()

@router.get("/{id}", response_model=Product, summary="Obter produto", description="Obtém detalhes de um produto específico")
def get_product(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{id}", response_model=Product, summary="Atualizar produto", description="Atualiza os dados de um produto")
def update_product(id: int, product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not validate_barcode(product.barcode):
        raise HTTPException(status_code=400, detail="Invalid barcode")
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product_check = db.query(Product).filter(Product.barcode == product.barcode, Product.id != id).first()
    if db_product_check:
        raise HTTPException(status_code=400, detail="Barcode already registered")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{id}", summary="Deletar produto", description="Remove um produto (somente admin)")
def delete_product(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}