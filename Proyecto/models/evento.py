from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List


class LocalBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100)
    descripcion: Optional[str] = Field(
        default="Local amplio y cómodo, capacidad aprox. 150 personas.", max_length=500)


class Local(LocalBase, table=True):
    __tablename__ = "locales"
    id: int | None = Field(default=None, primary_key=True)
    salas: List["Sala"] = Relationship(back_populates="local")


class SalaBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100)
    capacidad: int = Field(default=150)
    local_id: int = Field(foreign_key="locales.id")


class Sala(SalaBase, table=True):
    __tablename__ = "salas"
    id: int | None = Field(default=None, primary_key=True)
    local: Optional[Local] = Relationship(back_populates="salas")
    reservaciones: List["Reservacion"] = Relationship(back_populates="sala")


class ReservacionProductoLink(SQLModel, table=True):
    __tablename__ = "reservacion_producto"
    reservacion_id: int | None = Field(
        default=None, foreign_key="reservaciones.id", primary_key=True)
    producto_id: int | None = Field(
        default=None, foreign_key="productos.id", primary_key=True)
    cantidad: int = Field(default=1)


class ReservacionBase(SQLModel):
    usuario_id: int = Field(foreign_key="usuarios.id")
    local_id: int = Field(foreign_key="locales.id")
    sala_id: int = Field(foreign_key="salas.id")
    fecha_evento: datetime
    hora_evento: str = Field(max_length=10)
    cantidad_personas: int = Field(gt=0)
    total: float = Field(default=0)
    estado: str = Field(default="Confirmada", max_length=50)


class Reservacion(ReservacionBase, table=True):
    __tablename__ = "reservaciones"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    sala: Optional[Sala] = Relationship(back_populates="reservaciones")
    productos: List["Producto"] = Relationship(
        link_model=ReservacionProductoLink)


class ReservacionCreate(SQLModel):
    local_id: int
    sala_id: int
    fecha_evento: datetime
    hora_evento: str
    cantidad_personas: int
    producto_ids: Optional[List[int]] = []


class ReservacionResponse(ReservacionBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}
