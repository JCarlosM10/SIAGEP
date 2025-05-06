from presupuesto.modelo import PresupuestoMensual, Transaccion_I, Transaccion_A, Transaccion_E

def agregar_transaccion(presupuesto, tipo, categoria, descripcion, monto, fecha, tipo_gasto=None):
    if tipo == "Ingreso":
        transaccion = Transaccion_I(tipo=tipo, categoria=categoria, descripcion=descripcion, monto=monto, fecha=fecha)
        presupuesto.ingresos.append(transaccion)
    elif tipo == "Egreso":
        transaccion = Transaccion_E(tipo=tipo, categoria=categoria, tipo_gasto=tipo_gasto ,descripcion=descripcion, monto=monto, fecha=fecha)
        presupuesto.egresos.append(transaccion)
    else:
        raise ValueError("Tipo de transacción inválido.")
    
def agregar_ahorro(presupuesto, tipo, monto, descripcion, fecha):
    transaccion = Transaccion_A(tipo=tipo, monto=monto, descripcion=descripcion, fecha=fecha)
    presupuesto.ahorros.append(transaccion)

def mostrar_resumen(presupuesto):
    print(f"--- Presupuesto de {presupuesto.mes} ---")
    print(f"Ingresos: ${sum(t.monto for t in presupuesto.ingresos):.2f}")
    print(f"Egresos: ${sum(t.monto for t in presupuesto.egresos):.2f}")
    print(f"Saldo actual: ${presupuesto.saldo_actual():.2f}")


