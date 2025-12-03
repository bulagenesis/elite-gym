# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Asegúrate de que todas estas importaciones son correctas
from app.routers import clientes, membresias, pagos, productos, users, venta

# 🚨 NUEVO: Importar Base y engine para la creación de tablas (TEMPORAL)
from app.database import Base, engine 

app = FastAPI(title="Elite Gym Backend")

# -----------------------------------------------------------------
# 🚨 NUEVO: PASO 1: CREACIÓN DE TABLAS AL INICIO (TEMPORAL)
# Esto soluciona el error "UndefinedTable" al crear las tablas en la DB de Render.
# ¡RECUERDA ELIMINAR ESTE BLOQUE DESPUÉS DE QUE FUNCIONE!
# -----------------------------------------------------------------
def create_database_tables():
    # Intenta crear todas las tablas definidas en Base.metadata
    Base.metadata.create_all(bind=engine)

create_database_tables()
print("Base de datos inicializada (Tablas creadas/verificadas).")
# -----------------------------------------------------------------


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