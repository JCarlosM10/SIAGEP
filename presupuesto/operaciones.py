from presupuesto.modelo import PresupuestoMensual, Transaccion
import datetime

def agregar_transaccion(presupuesto, tipo, categoria, monto):
    fecha = datetime.date.today()
    transaccion = Transaccion(tipo=tipo, categoria=categoria, monto=monto, fecha=fecha)
    
    if tipo == "ingreso":
        presupuesto.ingresos.append(transaccion)
    elif tipo == "egreso":
        presupuesto.egresos.append(transaccion)
    else:
        raise ValueError("Tipo de transacción inválido.")

def mostrar_resumen(presupuesto):
    print(f"--- Presupuesto de {presupuesto.mes} ---")
    print(f"Ingresos: ${sum(t.monto for t in presupuesto.ingresos):.2f}")
    print(f"Egresos: ${sum(t.monto for t in presupuesto.egresos):.2f}")
    print(f"Saldo actual: ${presupuesto.saldo_actual():.2f}")
