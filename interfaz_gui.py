import tkinter as tk
from tkinter import ttk, messagebox
from presupuesto.modelo import PresupuestoMensual
from presupuesto.operaciones import agregar_transaccion
from presupuesto.persistencia import cargar_presupuesto, guardar_presupuesto

ARCHIVO_JSON = "data/presupuesto.json" 

presupuesto = cargar_presupuesto(ARCHIVO_JSON)

def registrar():
    tipo = tipo_var.get()
    categoria = entrada_categoria.get()
    try:
        monto = float(entrada_monto.get())
    except ValueError:
        messagebox.showerror("Error", "El monto debe ser un número.")
        return

    agregar_transaccion(presupuesto, tipo, categoria, monto)
    guardar_presupuesto(presupuesto, ARCHIVO_JSON)
    messagebox.showinfo("Éxito", f"{tipo.capitalize()} registrado.")
    entrada_categoria.delete(0, tk.END)
    entrada_monto.delete(0, tk.END)
    actualizar_resultado()

def actualizar_resultado():
    resumen = f"Saldo actual: ${presupuesto.saldo_actual():.2f}\n\n"
    resumen += "Ingresos:\n"
    for t in presupuesto.ingresos:
        resumen += f"- {t.categoria}: ${t.monto:.2f}\n"
    resumen += "\nEgresos:\n"
    for t in presupuesto.egresos:
        resumen += f"- {t.categoria}: ${t.monto:.2f}\n"
    area_resultado.delete("1.0", tk.END)
    area_resultado.insert(tk.END, resumen)

# Ventana principal
ventana = tk.Tk()
ventana.title("SIAGEP - Presupuesto Personal")

# Tipo (ingreso/egreso)
tipo_var = tk.StringVar()
tipo_var.set("ingreso")
ttk.Label(ventana, text="Tipo de transacción:").pack()
ttk.Combobox(ventana, textvariable=tipo_var, values=["ingreso", "egreso"]).pack()

# Categoría
ttk.Label(ventana, text="Categoría:").pack()
entrada_categoria = ttk.Entry(ventana)
entrada_categoria.pack()

# Monto
ttk.Label(ventana, text="Monto:").pack()
entrada_monto = ttk.Entry(ventana)
entrada_monto.pack()

# Botón para registrar
ttk.Button(ventana, text="Registrar", command=registrar).pack(pady=10)

# Área de resultados
area_resultado = tk.Text(ventana, height=15, width=50)
area_resultado.pack()

# Iniciar
actualizar_resultado()
ventana.mainloop()
