from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from config.session_Dependencia import SessionDependencia
from config.permissions import RequireAutenticado, get_current_user, RequireAdmin
from models.evento import Local, Sala, Reservacion, ReservacionCreate, ReservacionResponse, ReservacionProductoLink
from models.usuario import Usuario
from models.producto import Producto

router = APIRouter()


@router.get("/eventos/locales", response_model=list[Local], summary="(S5) Consultar locales")
def get_locales(session: SessionDependencia):
    return session.exec(select(Local)).all()


@router.get("/eventos/locales/{local_id}/salas", response_model=list[Sala], summary="(S5) Consultar salas por local")
def get_salas(local_id: int, session: SessionDependencia):
    return session.exec(select(Sala).where(Sala.local_id == local_id)).all()


@router.post("/eventos/reservaciones", response_model=ReservacionResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RequireAutenticado)], summary="(S5) Reservar sala para evento")
def create_reservacion(datos: ReservacionCreate, session: SessionDependencia, usuario: Usuario = Depends(get_current_user)):
    # Control de disponibilidad (TDR)
    existente = session.exec(select(Reservacion).where(
        Reservacion.sala_id == datos.sala_id,
        Reservacion.fecha_evento == datos.fecha_evento,
        Reservacion.hora_evento == datos.hora_evento,
        Reservacion.estado == "Confirmada"
    )).first()
    if existente:
        raise HTTPException(
            status_code=409, detail="La sala ya está reservada para esta fecha y hora.")

    nueva_res = Reservacion(usuario_id=usuario.id, local_id=datos.local_id, sala_id=datos.sala_id, fecha_evento=datos.fecha_evento,
                            hora_evento=datos.hora_evento, cantidad_personas=datos.cantidad_personas, total=0, estado="Confirmada")
    session.add(nueva_res)
    session.flush()

    if datos.producto_ids:
        for pid in datos.producto_ids:
            producto = session.get(Producto, pid)
            if producto:
                session.add(ReservacionProductoLink(
                    reservacion_id=nueva_res.id, producto_id=pid, cantidad=1))

    session.commit()
    session.refresh(nueva_res)
    return ReservacionResponse.model_validate(nueva_res)
