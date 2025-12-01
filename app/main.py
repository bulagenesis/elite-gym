from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import clientes, membresias, pagos, productos, users, venta  # ← AGREGAR 'venta' AQUÍ

app = FastAPI(title="Elite Gym Backend")

# 🔧 CONFIGURACIÓN CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL de tu frontend React
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos los headers
)

# Incluir routers con sus prefijos correctos
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(membresias.router, prefix="/membresias", tags=["Membresias"])
app.include_router(pagos.router, prefix="/pagos", tags=["Pagos"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(venta.router, prefix="/ventas", tags=["Ventas"])  # ← AGREGAR ESTA LÍNEA

# Endpoint raíz
@app.get("/")
def root():
    return {"message": "Backend Elite Gym funcionando!"}