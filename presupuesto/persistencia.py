import pandas as pd
from presupuesto.modelo import PresupuestoMensual, Transaccion_I, Transaccion_A, Transaccion_E
from datetime import datetime

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
        "tipo de gasto": t.tipo_gasto,
        "descripcion": t.descripcion,
        "monto": t.monto,
        "fecha": t.fecha.isoformat()
    } for t in presupuesto.egresos])

    ahorros_df = pd.DataFrame([{
        "tipo": t.tipo,
        "monto": t.monto,
        "descripcion": t.descripcion,
        "fecha": t.fecha.isoformat()
    } for t in presupuesto.ahorros])

    with pd.ExcelWriter(archivo, engine="openpyxl") as writer:
        ingresos_df.to_excel(writer, sheet_name="Ingresos", index=False)
        egresos_df.to_excel(writer, sheet_name="Egresos", index=False)
        ahorros_df.to_excel(writer, sheet_name="Ahorros", index=False)

    print(f"Presupuesto guardado en {archivo}")

def cargar_desde_excel(archivo):
    presupuesto = PresupuestoMensual(mes="Mayo 2025")

    try:
        ingresos_df = pd.read_excel(archivo, sheet_name="Ingresos")
        egresos_df = pd.read_excel(archivo, sheet_name="Egresos")
        ahorros_df = pd.read_excel(archivo, sheet_name="Ahorros")

        for _, row in ingresos_df.iterrows():
            presupuesto.ingresos.append(Transaccion_I(
                tipo=row["tipo"],
                categoria=row["categoria"],
                descripcion=row["descripcion"],
                monto=row["monto"],
                fecha=datetime.fromisoformat(str(row["fecha"])).date()
            ))

        for _, row in egresos_df.iterrows():
            presupuesto.egresos.append(Transaccion_E(
                tipo=row["tipo"],
                categoria=row["categoria"],
                tipo_gasto=row["tipo de gasto"],
                descripcion=row["descripcion"],
                monto=row["monto"],
                fecha=datetime.fromisoformat(str(row["fecha"])).date()
            ))

        for _, row in ahorros_df.iterrows():
            presupuesto.ahorros.append(Transaccion_A(
                tipo=row["tipo"],
                monto=row["monto"],
                descripcion=row["descripcion"],
                fecha=datetime.fromisoformat(str(row["fecha"])).date()
            ))

        print(f"Presupuesto cargado desde {archivo}")
    except FileNotFoundError:
        print("⚠️ Archivo Excel no encontrado. Se inicia un presupuesto vacío.")

    return presupuesto
