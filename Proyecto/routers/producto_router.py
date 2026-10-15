# routers/producto_router.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from models.producto import Producto, ProductoCreate, ProductoResponse, Categoria, CategoriaCreate
from services.database import get_session
from services.auth import get_current_user, get_current_admin
from models.usuario import Usuario

router = APIRouter(prefix="/api/productos", tags=["Catálogo"])

# ==========================================
# RUTAS PÚBLICAS (Cualquiera puede ver)
# ==========================================

@router.get("/", response_model=List[ProductoResponse])
def obtener_productos(session: Session = Depends(get_session)):
    """Cualquiera puede ver los productos disponibles"""
    statement = select(Producto).where(Producto.disponible == True)
    productos = session.exec(statement).all()
    return productos

@router.get("/categorias", response_model=List[Categoria])
def obtener_categorias(session: Session = Depends(get_session)):
    """Cualquiera puede ver las categorías"""
    statement = select(Categoria)
    categorias = session.exec(statement).all()
    return categorias


# ==========================================
# RUTAS DE CLIENTE (Requiere estar logueado)
# ==========================================

@router.get("/mis-pedidos", response_model=List[dict])
def obtener_mis_pedidos(
    current_user: Usuario = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """El cliente puede ver sus propios pedidos"""
    # Aquí iría la lógica para obtener pedidos del usuario
    return [{"mensaje": f"Pedidos de {current_user.nombre}"}]


# ==========================================
# RUTAS DE ADMINISTRADOR (Solo admin puede acceder)
# ==========================================

@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(
    data: ProductoCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin)  # ← Solo admin
):
    """Solo el administrador puede crear productos"""
    nuevo_producto = Producto(**data.model_dump())
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)
    return nuevo_producto

@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int,
    data: ProductoCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin)  # ← Solo admin
):
    """Solo el administrador puede actualizar productos"""
    statement = select(Producto).where(Producto.id == producto_id)
    producto = session.exec(statement).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Actualizar campos
    producto.nombre = data.nombre
    producto.descripcion = data.descripcion
    producto.precio = data.precio
    producto.imagen = data.imagen
    producto.disponible = data.disponible
    producto.categoria_id = data.categoria_id
    
    session.add(producto)
    session.commit()
    session.refresh(producto)
    
    return producto

@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin)  # ← Solo admin
):
    """Solo el administrador puede eliminar productos"""
    statement = select(Producto).where(Producto.id == producto_id)
    producto = session.exec(statement).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    session.delete(producto)
    session.commit()
    
    return {"mensaje": "Producto eliminado con éxito"}