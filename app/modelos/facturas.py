from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

# Esto es necesario para que el tipado funcione sin causar errores de importación
if TYPE_CHECKING:
    from app.modelos.clientes import Cliente
    from app.modelos.transacciones import Transaccion

class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)
    cliente_id: Optional[int] = Field(default=None, foreign_key="cliente.id")

class Factura(FacturaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Usamos strings entre comillas para evitar el ciclo de importación
    cliente: Optional["Cliente"] = Relationship(back_populates="facturas")
    transacciones: List["Transaccion"] = Relationship(back_populates="factura")

    @property
    def valor_total(self) -> float:
        return sum(t.cantidad * t.valor_unitario for t in self.transacciones)

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(SQLModel):
    fecha: Optional[datetime] = None