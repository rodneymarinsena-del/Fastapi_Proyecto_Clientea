from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

# Importación para el tipado que no causa ciclos
if TYPE_CHECKING:
    from app.modelos.facturas import Factura

# 1. Base para validación
class TransaccionBase(SQLModel):
    cantidad: float
    valor_unitario: float

# 2. Clase para la base de datos (con table=True)
class Transaccion(TransaccionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    factura_id: Optional[int] = Field(default=None, foreign_key="factura.id")
    
    # Relación inversa usando string para evitar el error de importación
    factura: Optional["Factura"] = Relationship(back_populates="transacciones")

# 3. Esquemas para endpoints
class TransaccionCrear(TransaccionBase):
    pass

class TransaccionEditar(SQLModel):
    cantidad: Optional[float] = None
    valor_unitario: Optional[float] = None