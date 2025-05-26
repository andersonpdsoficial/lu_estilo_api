from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, Order, OrderItemCreate
from app.database.database import get_db
from app.utils.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order, summary="Criar pedido", description="Cria um novo pedido com múltiplos produtos, validando estoque")
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.description}")
    
    db_order = Order(client_id=order.client_id, user_id=current_user.id, status=OrderStatus.pending)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )
        product.stock -= item.quantity
        db.add(db_item)
    
    db.commit()
    return db_order

@router.get("/", response_model=List[Order], summary="Listar pedidos", description="Lista pedidos com filtros de período, seção, status, etc.")
def list_orders(
    skip: int = 0,
    limit: int = 10,
    start_date: datetime = None,
    end_date: datetime = None,
    section: str = None,
    order_id: int = None,
    status: OrderStatus = None,
    client_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Order)
    if start_date:
        query = query.filter(Order.created_at >= start_date)
    if end_date:
        query = query.filter(Order.created_at <= end_date)
    if order_id:
        query = query.filter(Order.id == order_id)
    if status:
        query = query.filter(Order.status == status)
    if client_id:
        query = query.filter(Order.client_id == client_id)
    if section:
        query = query.join(OrderItem).join(Product).filter(Product.section == section)
    return query.offset(skip).limit(limit).all()

@router.get("/{id}", response_model=Order, summary="Obter pedido", description="Obtém detalhes de um pedido específico")
def get_order(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{id}", response_model=Order, summary="Atualizar pedido", description="Atualiza um pedido, incluindo itens e status")
def update_order(id: int, order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_order = db.query(Order).filter(Order.id == id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Restaurar estoque dos itens existentes
    existing_items = db.query(OrderItem).filter(OrderItem.order_id == id).all()
    for item in existing_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock += item.quantity
        db.delete(item)
    
    # Validar novo estoque
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.description}")
    
    # Atualizar pedido
    for key, value in order.dict(exclude={"items"}).items():
        setattr(db_order, key, value)
    
    # Criar novos itens
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )
        product.stock -= item.quantity
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{id}", summary="Deletar pedido", description="Remove um pedido (somente admin)")
def delete_order(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted"}