# models/producto.py
from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime
from datetime import datetime

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"  # <--- IMPORTANTE
    id: int | None = Field(default=None, primary_key=True)
    nombre: str

class CategoriaCreate(SQLModel):
    nombre: str

class Producto(SQLModel, table=True):
    __tablename__ = "productos"  # <--- IMPORTANTE
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str | None = None
    precio: float
    imagen: str | None = None
    disponible: bool = True
    categoria_id: int = Field(foreign_key="categorias.id")
    creado_en: datetime | None = Field(default=None, sa_type=DateTime)

class ProductoCreate(SQLModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    imagen: str | None = None
    disponible: bool = True
    categoria_id: int

class ProductoResponse(SQLModel):
    id: int
    nombre: str
    descripcion: str | None = None
    precio: float
    imagen: str | None = None
    disponible: bool
    categoria_id: int