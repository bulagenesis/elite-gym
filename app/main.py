# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Asegúrate de que todas estas importaciones son correctas
from app.routers import clientes, membresias, pagos, productos, users, venta

app = FastAPI(title="Elite Gym Backend")

# -----------------------------------------------------------------
# 🔧 CONFIGURACIÓN CORS (Crucial para Vercel)
# -----------------------------------------------------------------

# Definición de los orígenes (dominios) que tienen permiso para llamar a esta API.
origins = [
    # 1. URL pública de tu frontend desplegado en Vercel
    "https://gimnasio-elite-frontend.vercel.app",
    
    # 2. URL de desarrollo local
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # Lista de dominios permitidos
    allow_credentials=True,             # Permite enviar credenciales (si las usas)
    allow_methods=["*"],                # Permite todos los métodos HTTP
    allow_headers=["*"],                # Permite todos los encabezados
)

# -----------------------------------------------------------------
# INCLUSIÓN DE ROUTERS
# -----------------------------------------------------------------

# Incluir routers con sus prefijos correctos
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(membresias.router, prefix="/membresias", tags=["Membresias"])
app.include_router(pagos.router, prefix="/pagos", tags=["Pagos"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(venta.router, prefix="/ventas", tags=["Ventas"]) 

# Endpoint raíz
@app.get("/")
def root():
    return {"message": "Backend Elite Gym funcionando!"}