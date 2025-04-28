from dataclasses import dataclass, field
from typing import List
import datetime

@dataclass
class Transaccion:
    tipo: str  # "ingreso" o "egreso"
    categoria: str
    descripcion: str
    monto: float
    fecha: datetime.date

@dataclass
class PresupuestoMensual:
    mes: str
    ingresos: List[Transaccion] = field(default_factory=list)
    egresos: List[Transaccion] = field(default_factory=list)

    def saldo_actual(self):
        total_ingresos = sum(t.monto for t in self.ingresos)
        total_egresos = sum(t.monto for t in self.egresos)
        return total_ingresos - total_egresos