# routers/usuario_router.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from datetime import datetime, timedelta
import bcrypt
import jwt
import os
import secrets

from models.usuario import Usuario, UsuarioCreate, UsuarioResponse, UsuarioLogin, Recuperacion, CambiarPassword
from services.database import get_session

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta_super_segura_2026")
ALGORITHM = "HS256"

# ==========================================
# 1. REGISTRO (Crear cuenta)
# ==========================================
@router.post("/registro", response_model=UsuarioResponse, status_code=201)
def registrar_usuario(data: UsuarioCreate, session: Session = Depends(get_session)):
    # Verificar si el correo ya existe
    statement = select(Usuario).where(Usuario.email == data.email)
    if session.exec(statement).first():
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Encriptar contraseña con bcrypt (Requisito del PDF)
    password_hash = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    nuevo_usuario = Usuario(
        nombre=data.nombre,
        email=data.email,
        password=password_hash,
        rol=data.rol or "cliente",
        creado_en=datetime.utcnow()
    )
    
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)

    return UsuarioResponse(id=nuevo_usuario.id, nombre=nuevo_usuario.nombre, email=nuevo_usuario.email, rol=nuevo_usuario.rol)


# ==========================================
# 2. LOGIN (Iniciar sesión)
# ==========================================
@router.post("/login")
def login(data: UsuarioLogin, session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.email == data.email)
    usuario = session.exec(statement).first()

    # Verificar usuario y contraseña con bcrypt
    if not usuario or not bcrypt.checkpw(data.password.encode('utf-8'), usuario.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Generar Token JWT (Requisito del PDF)
    token_data = {
        "id": usuario.id,
        "email": usuario.email,
        "rol": usuario.rol,
        "exp": datetime.utcnow() + timedelta(hours=24) # Expira en 24 horas
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": UsuarioResponse(id=usuario.id, nombre=usuario.nombre, email=usuario.email, rol=usuario.rol)
    }


# ==========================================
# 3. RECUPERAR CONTRASEÑA (Paso 1: Solicitar código)
# ==========================================
@router.post("/recuperar")
def recuperar_contraseña(data: Recuperacion, session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.email == data.email)
    usuario = session.exec(statement).first()

    if not usuario:
        # Por seguridad, no revelamos si el email existe o no
        return {"mensaje": "Si el correo está registrado, recibirás un código de recuperación."}

    # Generar token único de recuperación
    token_recuperacion = secrets.token_urlsafe(32)
    usuario.token_recuperacion = token_recuperacion
    session.add(usuario)
    session.commit()

    # NOTA: En un proyecto real, aquí se usaría una librería para enviar un email.
    # Para este proyecto académico, lo devolvemos en la respuesta para que puedas probarlo.
    return {
        "mensaje": "Código generado (simulación de envío de correo).",
        "token_recuperacion": token_recuperacion 
    }


# ==========================================
# 4. CAMBIAR CONTRASEÑA (Paso 2: Establecer nueva)
# ==========================================
@router.post("/cambiar-password")
def cambiar_password(data: CambiarPassword, session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.email == data.email)
    usuario = session.exec(statement).first()

    if not usuario or usuario.token_recuperacion != data.token:
        raise HTTPException(status_code=400, detail="Código de recuperación inválido o expirado")

    # Encriptar la nueva contraseña
    password_hash = bcrypt.hashpw(data.nueva_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    usuario.password = password_hash
    usuario.token_recuperacion = None  # Invalidar el código después de usarlo
    session.add(usuario)
    session.commit()

    return {"mensaje": "Contraseña actualizada con éxito"}