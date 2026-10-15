# models/usuario.py
from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime
from datetime import datetime

# 1. Tabla en la Base de Datos
class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"  # Nombre exacto en MySQL
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(unique=True, index=True)
    password: str
    rol: str = Field(default="cliente")
    token_recuperacion: str | None = None
    creado_en: datetime | None = Field(default=None, sa_type=DateTime)

# 2. Esquemas para la API
class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    password: str
    rol: str | None = "cliente"

class UsuarioResponse(SQLModel):
    id: int
    nombre: str
    email: str
    rol: str

class UsuarioLogin(SQLModel):
    email: str
    password: str

class Recuperacion(SQLModel):
    email: str

class CambiarPassword(SQLModel):
    email: str
    token: str
    nueva_password: str