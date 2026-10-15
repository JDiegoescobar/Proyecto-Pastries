# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import usuario_router, producto_router, evento_router, admin_router

app = FastAPI(
    title="Ríos Pastries API",
    description="Sistema de gestión de pedidos y eventos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar todos los routers
app.include_router(usuario_router.router)
app.include_router(producto_router.router)
app.include_router(evento_router.router)
app.include_router(admin_router.router)  # ← Agregado

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Ríos Pastries "}