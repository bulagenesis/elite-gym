from app.database import Base, engine
from app.models import cliente, membresia, pago, producto, user  # importa todos los modelos

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente")
