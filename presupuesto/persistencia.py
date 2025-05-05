import json
import pandas as pd
from presupuesto.modelo import PresupuestoMensual, Transaccion
from datetime import date, datetime

def guardar_en_excel(presupuesto, archivo="data/presupuesto.xlsx"):
    ingresos_df = pd.DataFrame([{
        "tipo": t.tipo,
        "categoria": t.categoria,
        "descripcion": t.descripcion,
        "monto": t.monto,
        "fecha": t.fecha.isoformat()
    } for t in presupuesto.ingresos])

    egresos_df = pd.DataFrame([{
        "tipo": t.tipo,
        "categoria": t.categoria,
        "descripcion": t.descripcion,
        "monto": t.monto,
        "fecha": t.fecha.isoformat()
    } for t in presupuesto.egresos])

    with pd.ExcelWriter(archivo, engine="openpyxl") as writer:
        ingresos_df.to_excel(writer, sheet_name="Ingresos", index=False)
        egresos_df.to_excel(writer, sheet_name="Egresos", index=False)

    print(f"Presupuesto guardado en {archivo}")

def cargar_desde_excel(archivo="data/presupuesto.xlsx"):
    presupuesto = PresupuestoMensual(mes="Mayo 2025")

    try:
        ingresos_df = pd.read_excel(archivo, sheet_name="Ingresos")
        egresos_df = pd.read_excel(archivo, sheet_name="Egresos")

        for _, row in ingresos_df.iterrows():
            presupuesto.ingresos.append(Transaccion(
                tipo=row["tipo"],
                categoria=row["categoria"],
                descripcion=row["descripcion"],
                monto=row["monto"],
                fecha=datetime.fromisoformat(str(row["fecha"])).date()
            ))

        for _, row in egresos_df.iterrows():
            presupuesto.egresos.append(Transaccion(
                tipo=row["tipo"],
                categoria=row["categoria"],
                descripcion=row["descripcion"],
                monto=row["monto"],
                fecha=datetime.fromisoformat(str(row["fecha"])).date()
            ))

        print(f"📂 Presupuesto cargado desde {archivo}")
    except FileNotFoundError:
        print("⚠️ Archivo Excel no encontrado. Se inicia un presupuesto vacío.")

    return presupuesto

'''
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
    
def guardar_presupuesto(presupuesto, archivo="data/presupuesto.json"):
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
'''