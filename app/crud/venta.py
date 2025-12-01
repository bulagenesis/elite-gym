from sqlalchemy.orm import Session, joinedload
from app.models.venta import Venta, ProductoVendido
from app.models.producto import Producto
from app.schemas.venta import VentaCreate
from datetime import datetime

def crear_venta(db: Session, venta: VentaCreate):
    try:
        # Validar productos y calcular total
        total = 0
        productos_a_vender = []
        
        for item in venta.productos:
            producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
            if not producto:
                raise ValueError(f"Producto con ID {item.producto_id} no encontrado")
            
            if producto.stock < item.cantidad:
                raise ValueError(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
            
            subtotal = item.cantidad * item.precio_unitario
            total += subtotal
            
            productos_a_vender.append({
                'producto': producto,
                'cantidad': item.cantidad,
                'precio_unitario': item.precio_unitario,
                'subtotal': subtotal
            })
        
        # Crear venta
        db_venta = Venta(
            fecha_venta=datetime.now(),
            total=total,
            metodo_pago=venta.metodo_pago,
            cliente_id=venta.cliente_id
        )
        db.add(db_venta)
        db.flush()  # Para obtener el ID de la venta
        
        # Crear productos vendidos y actualizar stock
        for item in productos_a_vender:
            db_producto_vendido = ProductoVendido(
                venta_id=db_venta.id,
                producto_id=item['producto'].id,
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario'],
                subtotal=item['subtotal']
            )
            db.add(db_producto_vendido)
            
            # Actualizar stock
            item['producto'].stock -= item['cantidad']
        
        db.commit()
        
        # 🔥 CARGAR RELACIONES PARA LA RESPUESTA
        db.refresh(db_venta)
        venta_con_relaciones = (
            db.query(Venta)
            .options(
                joinedload(Venta.productos)
                .joinedload(ProductoVendido.producto)
            )
            .filter(Venta.id == db_venta.id)
            .first()
        )
        
        return venta_con_relaciones
        
    except Exception as e:
        db.rollback()
        raise e

def obtener_ventas(db: Session, skip: int = 0, limit: int = 100):
    # 🔥 CARGAR TODAS LAS RELACIONES NECESARIAS
    return (
        db.query(Venta)
        .options(
            joinedload(Venta.productos)
            .joinedload(ProductoVendido.producto)
        )
        .order_by(Venta.fecha_venta.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def obtener_venta_por_id(db: Session, venta_id: int):
    # 🔥 CARGAR RELACIONES PARA UNA VENTA ESPECÍFICA
    return (
        db.query(Venta)
        .options(
            joinedload(Venta.productos)
            .joinedload(ProductoVendido.producto)
        )
        .filter(Venta.id == venta_id)
        .first()
    )