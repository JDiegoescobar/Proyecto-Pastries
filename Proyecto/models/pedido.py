from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum
import sqlalchemy as sa


class EstadoPedido(str, Enum):
    PENDIENTE = "Pendiente"
    EN_PREPARACION = "En preparación"
    LISTO = "Listo"
    ENTREGADO = "Entregado"


class TipoEntrega(str, Enum):
    RETIRO = "Recoger en local"
    DOMICILIO = "Entrega a domicilio"


class MetodoPago(str, Enum):
    EFECTIVO = "Efectivo"
    TARJETA = "Tarjeta"
    TRANSFERENCIA = "Transferencia"


class PedidoProductoLink(SQLModel, table=True):
    __tablename__ = "pedido_producto"
    pedido_id: int | None = Field(
        default=None, foreign_key="pedidos.id", primary_key=True)
    producto_id: int | None = Field(
        default=None, foreign_key="productos.id", primary_key=True)
    cantidad: int = Field(default=1)
    precio_unitario: float = Field(default=0)


class PedidoBase(SQLModel):
    usuario_id: int = Field(foreign_key="usuarios.id")
    tipo_entrega: TipoEntrega
    direccion: Optional[str] = Field(default=None, max_length=255)
    metodo_pago: MetodoPago
    subtotal: float = Field(nullable=False, ge=0)
    total: float = Field(nullable=False, gt=0)
    estado: EstadoPedido = Field(default=EstadoPedido.PENDIENTE, sa_column=sa.Column(
        sa.String(20), nullable=False, server_default="Pendiente"))


class Pedido(PedidoBase, table=True):
    __tablename__ = "pedidos"
    id: int | None = Field(default=None, primary_key=True)
    fecha_hora: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    productos: List["Producto"] = Relationship(link_model=PedidoProductoLink)


class PedidoCreate(SQLModel):
    producto_ids: List[int]
    cantidades: List[int]
    tipo_entrega: TipoEntrega
    direccion: Optional[str] = None
    metodo_pago: MetodoPago


class PedidoResponse(PedidoBase):
    id: int
    fecha_hora: datetime
    created_at: datetime
    model_config = {"from_attributes": True}
