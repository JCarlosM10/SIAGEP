from presupuesto.modelo import PresupuestoMensual
from presupuesto.operaciones import agregar_transaccion, agregar_ahorro
from presupuesto.persistencia import cargar_desde_excel, guardar_en_excel

ARCHIVO_EXCEL = "data/presupuesto.xlsx"

def cargar_presupuesto():
    try:
        return cargar_desde_excel(ARCHIVO_EXCEL)
    except FileNotFoundError:
        return PresupuestoMensual()

def guardar_presupuesto(presupuesto):
    guardar_en_excel(presupuesto, ARCHIVO_EXCEL)

def registrar_transaccion(presupuesto, tipo, categoria, descripcion, monto, fecha, tipo_gasto):
    agregar_transaccion(presupuesto, tipo, categoria, descripcion, monto, fecha, tipo_gasto)
    guardar_presupuesto(presupuesto)

def registrar_ahorro(presupuesto, monto, descripcion, fecha):
    agregar_ahorro(presupuesto, "Ahorro", monto, descripcion, fecha)
    guardar_presupuesto(presupuesto)