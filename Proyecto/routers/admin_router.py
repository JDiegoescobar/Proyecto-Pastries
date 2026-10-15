# routers/admin_router.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from models.usuario import Usuario, UsuarioResponse
from models.producto import Producto, ProductoResponse, Categoria
from models.evento import Local, Sala
from services.database import get_session
from services.auth import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Panel Administrativo"])


# ==========================================
# USUARIOS (Clientes)
# ==========================================

@router.get("/usuarios", response_model=List[UsuarioResponse])
def listar_usuarios(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin)
):
    """El admin puede ver todos los clientes registrados"""
    statement = select(Usuario).where(Usuario.rol == "cliente")
    usuarios = session.exec(statement).all()
    return usuarios


# ==========================================
# PRODUCTOS
# ==========================================

@router.get("/productos", response_model=List[ProductoResponse])
def admin_listar_productos(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin)
):
    """El admin puede ver todos los productos (incluidos no disponibles)"""
    statement = select(Producto)
    productos = session.exec(statement).all()
    return productos


# ==========================================
# CATEGORÍAS
# ==========================================

@router.get("/categorias", response_model=List[Categoria])
def admin_listar_categorias(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin)
):
    """El admin puede gestionar categorías"""
    statement = select(Categoria)
    return session.exec(statement).all()

@router.post("/categorias", response_model=Categoria, status_code=201)
def admin_crear_categoria(
    nombre: str,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin)
):
    """El admin puede crear nuevas categorías"""
    categoria = Categoria(nombre=nombre)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


# ==========================================
# LOCALES Y SALAS
# ==========================================

@router.get("/locales", response_model=List[Local])
def admin_listar_locales(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin)
):
    """El admin puede ver y gestionar locales"""
    statement = select(Local)
    return session.exec(statement).all()

@router.get("/salas", response_model=List[Sala])
def admin_listar_salas(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin)
):
    """El admin puede ver y gestionar salas"""
    statement = select(Sala)
    return session.exec(statement).all()