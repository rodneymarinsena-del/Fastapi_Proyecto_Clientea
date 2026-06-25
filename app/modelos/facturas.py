from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# ESTO ES LA CLAVE: 
# Usar TYPE_CHECKING evita que se ejecuten los imports durante la carga del programa
if TYPE_CHECKING:
    from app.modelos.clientes import Cliente
    from app.modelos.transacciones import Transaccion
    from app.modelos.clientes import ClienteLeer
    from app.modelos.transacciones import TransaccionLeer

class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)
    cliente_id: Optional[int] = Field(default=None, foreign_key="cliente.id")

class Factura(FacturaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # IMPORTANTE: Usa strings entre comillas ("Cliente", "Transaccion")
    # Nunca uses la clase directa aquí si causa importación circular
    cliente: Optional["Cliente"] = Relationship(back_populates="facturas")
    transacciones: List["Transaccion"] = Relationship(back_populates="factura")

    @property
    def valor_total(self) -> float:
        return sum(t.cantidad * t.valor_unitario for t in self.transacciones)

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(SQLModel):
    fecha: Optional[datetime] = None

class FacturaLeer(FacturaBase):
    id: int
    cliente: Optional["ClienteLeer"] = None
    transacciones: List["TransaccionLeer"] = []

from app.modelos.clientes import ClienteLeer
from app.modelos.transacciones import TransaccionLeer

FacturaLeer.model_rebuild()