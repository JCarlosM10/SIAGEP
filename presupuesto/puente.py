from presupuesto.modelo import PresupuestoMensual, Transaccion_A, Transaccion_I, Transaccion_E
from presupuesto.sqlite import insertar_transaccion, insertar_ahorro, obtener_transacciones, obtener_ahorros
from datetime import datetime

def cargar_presupuesto():
    presupuesto = PresupuestoMensual(mes = 'Junio 2025')
    transacciones = obtener_transacciones()
    ahorros = obtener_ahorros()

    for transaccion in transacciones:
        tipo, categoria, descripcion, monto, fecha, tipo_gasto = transaccion[1:]
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        if tipo == 'Ingreso':
            presupuesto.ingresos.append(Transaccion_I(tipo, categoria, descripcion, monto, fecha))
        elif tipo == 'Egreso':
            presupuesto.egresos.append(Transaccion_E(tipo, categoria, descripcion, monto, fecha, tipo_gasto))
    
    for ahorro in ahorros:
        tipo, descripcion, monto, fecha = ahorro[1:]
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date() 
        if tipo == 'Ahorro':
            presupuesto.ahorros.append(Transaccion_A(tipo, descripcion, monto, fecha))

    return presupuesto


def registrar_transaccion(presupuesto, tipo, categoria, descripcion, monto, fecha, tipo_gasto):
    insertar_transaccion(tipo, categoria, descripcion, monto, fecha, tipo_gasto)
    if tipo == 'Ingreso':
        presupuesto.ingresos.append(Transaccion_I(tipo, categoria, descripcion, monto, fecha))
    elif tipo == 'Egreso':
        presupuesto.egresos.append(Transaccion_E(tipo, categoria, descripcion, monto, fecha, tipo_gasto))
    
def registrar_ahorro(presupuesto, tipo, descripcion, monto, fecha):
    insertar_ahorro(tipo, descripcion, monto, fecha)
    presupuesto.ahorros.append(Transaccion_A(tipo, descripcion, monto, fecha))