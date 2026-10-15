from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from config.session_Dependencia import SessionDependencia
from config.permissions import RequireAutenticado, get_current_user, RequireAdmin
from models.pedido import Pedido, PedidoCreate, PedidoResponse, EstadoPedido, TipoEntrega, PedidoProductoLink
from models.usuario import Usuario, RolUsuario
from models.producto import Producto
from lib.utils import is_horario_atencion

router = APIRouter()


@router.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RequireAutenticado)], summary="(S4) Crear pedido en línea")
def create_pedido(datos: PedidoCreate, session: SessionDependencia, usuario: Usuario = Depends(get_current_user)):
    if not is_horario_atencion():
        raise HTTPException(
            status_code=403, detail="El negocio está CERRADO. Horario de pedidos: 9:00 a.m. a 7:00 p.m.")
    if datos.tipo_entrega == TipoEntrega.DOMICILIO and not datos.direccion:
        raise HTTPException(
            status_code=400, detail="La dirección es obligatoria para entrega a domicilio.")

    subtotal = 0.0
    nuevo_pedido = Pedido(usuario_id=usuario.id, tipo_entrega=datos.tipo_entrega, direccion=datos.direccion,
                          metodo_pago=datos.metodo_pago, subtotal=0, total=0, estado=EstadoPedido.PENDIENTE)
    session.add(nuevo_pedido)
    session.flush()

    for prod_id, cantidad in zip(datos.producto_ids, datos.cantidades):
        producto = session.get(Producto, prod_id)
        if not producto or not producto.disponible:
            raise HTTPException(
                status_code=400, detail=f"Producto {prod_id} no disponible")
        subtotal += producto.precio * cantidad
        session.add(PedidoProductoLink(pedido_id=nuevo_pedido.id,
                    producto_id=prod_id, cantidad=cantidad, precio_unitario=producto.precio))

    nuevo_pedido.subtotal = subtotal
    nuevo_pedido.total = subtotal
    session.commit()
    session.refresh(nuevo_pedido)
    return PedidoResponse.model_validate(nuevo_pedido)


@router.patch("/pedidos/{pedido_id}/estado", dependencies=[Depends(RequireAdmin)], summary="(S4) Actualizar estado del pedido (Admin)")
def update_estado_pedido(pedido_id: int, estado: EstadoPedido, session: SessionDependencia):
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido.estado = estado
    session.commit()
    return {"message": f"Estado actualizado a: {estado.value}"}
