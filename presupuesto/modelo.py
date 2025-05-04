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
    aportaciones_ahorro: List[float] = field(default_factory=list)

    def saldo_actual(self):
        total_ingresos = sum(t.monto for t in self.ingresos)
        total_egresos = sum(t.monto for t in self.egresos)
        return total_ingresos - total_egresos
    
    def totales(self):
        total_ingresos = sum(t.monto for t in self.ingresos)
        total_egresos = sum(t.monto for t in self.egresos)
        total_aportaciones = sum(self.aportaciones_ahorro)
        return total_ingresos, total_egresos, total_aportaciones
    
    def distribucion_gastos(self):
        total_ingresos = sum(t.monto for t in self.ingresos)
        if total_ingresos == 0:
            return 0,0,0
        fijo_obligatorio = sum(t.monto for t in self.egresos if t.categoria in ["Vivienda", "Prestamo"])
        fijo_necesario = sum(t.monto for t in self.egresos if t.categoria in ["Alimentación", "Transporte", "Salud", "Educación", "Internet", "Luz", "Agua", "Gas"])
        variable = sum(t.monto for t in self.egresos if t.categoria in ["Entretenimiento", "Viajes", "Otros"])
        per_obligatorio = (fijo_obligatorio/total_ingresos)*100
        per_necesario = (fijo_necesario/total_ingresos)*100
        per_variable = (variable/total_ingresos)*100
        return per_obligatorio, per_necesario, per_variable
    
    def distribucion_ahorros(self):
        total_ingresos = sum(t.monto for t in self.ingresos)
        if total_ingresos == 0:
            return 0,0
        ahorro = sum(self.aportaciones_ahorro)
        saldo_actual = self.saldo_actual()
        per_ahorro = (ahorro/total_ingresos)*100
        per_gastos = (saldo_actual/total_ingresos)*100
        return per_ahorro, per_gastos
