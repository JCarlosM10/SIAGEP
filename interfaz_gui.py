import tkinter as tk
from tkinter import ttk, messagebox,scrolledtext
from datetime import datetime
from presupuesto.modelo import PresupuestoMensual
from presupuesto.operaciones import agregar_transaccion
from presupuesto.persistencia import cargar_desde_excel, guardar_en_excel

ARCHIVO_EXCEL = "data/presupuesto.xlsx" 

presupuesto = cargar_desde_excel(ARCHIVO_EXCEL)


def registrar():
    tipo = tipo_var.get()
    if tipo == "Seleccionar":
        messagebox.showerror("Error", "Seleccione un tipo de transacción.")
        return
    
    categoria = entrada_categoria.get()
    if categoria == "Seleccionar":
        messagebox.showerror("Error", "Seleccione una categoría.")
        return

    fecha = entrada_fecha.get() if not fecha_actual.get() else datetime.today().strftime("%d-%m-%Y")

    if not fecha_actual.get():
        try:
            fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
            fecha = fecha_obj.date()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use DD-MM-AAAA.")
            return
    else:
        fecha = datetime.today().date()
    
    if not fecha:
        messagebox.showerror("Error", "La fecha no puede estar vacía.")
        return

    descripcion = entrada_descripcion.get()
    if not descripcion:
        messagebox.showerror("Error", "Escribe una descripción.")
        return

    try:
        monto = float(entrada_monto.get())
    except ValueError:
        messagebox.showerror("Error", "El monto debe ser un número.")
        return

    agregar_transaccion(presupuesto, tipo, categoria, descripcion, monto, fecha)
    guardar_en_excel(presupuesto, ARCHIVO_EXCEL)
    messagebox.showinfo("Éxito", f"{tipo.capitalize()} registrado.")
    tipo_var.set("Seleccionar")
    entrada_categoria.set("Seleccionar")
    entrada_descripcion.delete(0, tk.END)
    entrada_monto.delete(0, tk.END)
    fecha_actual.set(False)
    entrada_fecha.delete(0, tk.END)
    actualizar_resultado()

def actualizar_resultado():
    total_width = 60
    hora_actual = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    resumen = f"Saldo actual (al {hora_actual}): \n${presupuesto.saldo_actual():.2f}\n\n"

    ingresos_ordenados = sorted(presupuesto.ingresos, key=lambda x: x.fecha)
    resumen += "Ingresos:\n"
    for t in ingresos_ordenados:
        fecha_user = t.fecha.strftime("%d-%m-%Y")
        line = f"- {t.categoria:<15} | {t.descripcion}: ${t.monto:.2f}"
        resumen += f"{line:<{total_width-5}}{fecha_user:>25}\n"
    egresos_ordenados = sorted(presupuesto.egresos, key=lambda x: x.fecha)  
    resumen += "\nEgresos:\n"
    for t in egresos_ordenados:
        fecha_user = t.fecha.strftime("%d-%m-%Y")
        line = f"- {t.categoria:<15} | {t.descripcion}: ${t.monto:.2f}"
        resumen += f"{line:<{total_width-5}}{fecha_user:>25}\n"

    area_resultado.config(state="normal")    
    area_resultado.delete("1.0", tk.END)
    area_resultado.insert(tk.END, resumen)
    area_resultado.config(state="disabled")

# Ventana principal
ventana = tk.Tk()
ventana.title("SIAGEP - Presupuesto Personal")
ventana.minsize(610,400)

# Tipo (ingreso/egreso)
tipo_var = tk.StringVar()
tipo_var.set("Seleccionar")
ttk.Label(ventana, text="Tipo de transacción:").pack()
ttk.Combobox(ventana, textvariable=tipo_var, values=["Ingreso", "Egreso"],state="readonly").pack()

#Fecha

def toggle_entrada_fecha(*args):
    if fecha_actual.get():
        entrada_fecha.pack_forget()
    else:
        entrada_fecha.pack(after=check_fecha)

ttk.Label(ventana, text="Fecha (DD-MM-AAAA):").pack()
fecha_actual = tk.BooleanVar(value=False)
fecha_actual.trace_add("write", toggle_entrada_fecha)
entrada_fecha = ttk.Entry(ventana)                                                          # Entry fecha

check_fecha = ttk.Checkbutton(ventana, text="Usar fecha actual", variable=fecha_actual)     # Checkbox
check_fecha.pack()

toggle_entrada_fecha()


#Frame para datos de entrada
frame_inputs = ttk.Frame(ventana)
frame_inputs.pack(pady=10, padx=10, fill="x")

# Categoría
ttk.Label(frame_inputs, text="Categoría:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
categorias_ing = ["Salario", "Horas extras", "Inversiones", "Otros"]
categorias_eg = ["Alimentos", "Vivienda" ,"Transporte", "Entretenimiento", "Salud", "Educación", "Otros"]
categoria_var = tk.StringVar()
categoria_var.set("Seleccionar")
entrada_categoria = ttk.Combobox(frame_inputs, textvariable=categoria_var, state="readonly")
entrada_categoria.grid(row=0, column=1, sticky="e", padx=20, pady=5)

def actualizar_categorias(*args):
    tipo = tipo_var.get()
    if tipo == "Ingreso":
        entrada_categoria['values'] = categorias_ing
    elif tipo == "Egreso":
        entrada_categoria['values'] = categorias_eg
    else:
        entrada_categoria['values'] = []
tipo_var.trace("w", actualizar_categorias)

#Descripción
ttk.Label(frame_inputs, text="Descripción:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entrada_descripcion = ttk.Entry(frame_inputs)
entrada_descripcion.grid(row=1, column=1, sticky="e", padx=20, pady=5)

# Monto
ttk.Label(frame_inputs, text="Monto:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entrada_monto = ttk.Entry(frame_inputs)
entrada_monto.grid(row=2, column=1, sticky="e", padx=20, pady=5)

# Botón para registrar
ttk.Button(ventana, text="Registrar", command=registrar).pack(pady=10)

# Área de resultados
area_resultado = scrolledtext.ScrolledText(ventana, width=50, height=15)
area_resultado.pack(pady=10, padx=10, fill="both", expand=True)

# Iniciar
actualizar_resultado()
ventana.mainloop()
