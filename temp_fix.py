# temp_fix.py - CREA ESTE ARCHIVO en elite-gym/
from app.database import SessionLocal, engine
from app.models.producto import Producto
import app.models.producto

print("🔄 Refrescando schema de la base de datos...")

# Fuerza el refresh completo
Producto.metadata.reflect(bind=engine, extend_existing=True)
Producto.metadata.create_all(bind=engine)

print("✅ Schema refrescado exitosamente!")
print("🎯 Ahora reinicia el servidor FastAPI")