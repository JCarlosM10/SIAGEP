import json
from presupuesto.modelo import PresupuestoMensual, Transaccion
from datetime import date, datetime

def transaccion_a_dict(transaccion):
    return {
        "tipo": transaccion.tipo,
        "categoria": transaccion.categoria,
        "descripcion": transaccion.descripcion,
        "monto": transaccion.monto,
        "fecha": transaccion.fecha.isoformat()
    }

def dict_a_transaccion(d):
    return Transaccion(
        tipo=d["tipo"],
        categoria=d["categoria"],
        descripcion=d["descripcion"],
        monto=d["monto"],
        fecha=datetime.fromisoformat(d["fecha"]).date()
    )

def guardar_presupuesto(presupuesto, archivo="SIAGEP/data/presupuesto.json"):
    data = {
        "mes": presupuesto.mes,
        "ingresos": [transaccion_a_dict(t) for t in presupuesto.ingresos],
        "egresos": [transaccion_a_dict(t) for t in presupuesto.egresos],
    }
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Presupuesto guardado en {archivo}")

def cargar_presupuesto(archivo="data/presupuesto.json"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
        presupuesto = PresupuestoMensual(mes=data["mes"])
        presupuesto.ingresos = [dict_a_transaccion(d) for d in data["ingresos"]]
        presupuesto.egresos = [dict_a_transaccion(d) for d in data["egresos"]]
        print(f"📂 Presupuesto cargado desde {archivo}")
        return presupuesto
    except FileNotFoundError:
        print("📁 Archivo no encontrado. Se creará un nuevo presupuesto.")
        return PresupuestoMensual(mes="Abril 2025")
