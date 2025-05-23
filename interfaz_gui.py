import tkinter as tk 
from tkinter import ttk, messagebox,scrolledtext 
from datetime import datetime 
from presupuesto.puente import cargar_presupuesto, registrar_transaccion, registrar_ahorro 

ARCHIVO_EXCEL = "data/presupuesto.xlsx" 
presupuesto = cargar_presupuesto()

# Funciones para registros y actualizaciones
# Función para registrar transacciones
def registrar():
    tipo = tipo_var.get()
    if tipo == "Seleccionar":
        messagebox.showerror("Error", "Seleccione un tipo de transacción.")
        return
    
    categoria = entrada_categoria.get()
    if categoria == "Seleccionar":
        messagebox.showerror("Error", "Seleccione una categoría.")
        return
    
    tipo_gasto = tipo_gasto_var.get()
    if tipo == "Egreso" and not tipo_gasto:
        messagebox.showerror("Error", "El tipo de gasto no puede estar vacío.")
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

    registrar_transaccion(presupuesto, tipo, categoria, descripcion, monto, fecha, tipo_gasto) 
    messagebox.showinfo("Éxito", f"{tipo.capitalize()} registrado.")
    tipo_var.set("Seleccionar")
    entrada_categoria.set("Seleccionar")
    entrada_descripcion.delete(0, tk.END)
    entrada_monto.delete(0, tk.END)
    fecha_actual.set(True)
    entrada_fecha.delete(0, tk.END)
    actualizar_resultado()

# Función para registrar aportaciones al ahorro
def registrar_aportacion():
    tipo = "Ahorro"
    try:
        monto_aportacion = float(entrada_aportacion.get())
        if monto_aportacion < 0:
            messagebox.showerror("Error", "El monto de la aportación no puede ser negativo.")
            return
    except ValueError:
        messagebox.showerror("Error", "Ingrese un monto válido para la aportación.")

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
    
    descripcion_ahorro = entrada_descripcion_ahorro.get()
    if not descripcion_ahorro:
        messagebox.showerror("Error", "Escribe una descripción.")
        return

    registrar_ahorro(presupuesto, monto_aportacion, descripcion_ahorro, fecha)
    messagebox.showinfo("Éxito", f"Aportación al ahorro registrada: ${monto_aportacion:.2f}")
    entrada_aportacion.delete(0, tk.END)
    entrada_descripcion_ahorro.delete(0, tk.END)
    fecha_actual.set(True)
    entrada_fecha.delete(0, tk.END)
    actualizar_resultado()

def actualizar_resultado():
    total_width = 60
    hora_actual = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    resumen = f"Movimientos al {hora_actual}\n\n"

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
    ahorros_ordenados = sorted(presupuesto.ahorros, key=lambda x: x.fecha)
    resumen += "\nAportaciones al Ahorro:\n"
    for t in ahorros_ordenados:
        fecha_user = t.fecha.strftime("%d-%m-%Y")
        line = f"- {t.descripcion}: ${t.monto:.2f}"
        resumen += f"{line:<{total_width-5}}{fecha_user:>25}\n"

    area_resultado.config(state="normal")    
    area_resultado.delete("1.0", tk.END)
    area_resultado.insert(tk.END, resumen)
    area_resultado.config(state="disabled")

    total_ingresos, total_egresos, total_ahorros = presupuesto.totales()
    label_total_ingresos.config(text=f"Total de Ingresos:\n{'${:.2f}'.format(total_ingresos).center(22)}")
    label_total_egresos.config(text=f"Total de Gastos:\n{'${:.2f}'.format(total_egresos).center(20)}")
    label_total_ahorros.config(text=f"Aportaciones al Ahorro:\n{'${:.2f}'.format(total_ahorros).center(35)}")
    label_saldo_actual.config(text=f"Saldo Actual:\n{'${:.2f}'.format(presupuesto.saldo_actual()).center(15)}")

    actualizar_porcentajes()

# Funciones para acciones de la interfaz
# Función para mostrar u ocultar la entrada de fecha
def toggle_entrada_fecha(*args):
    if fecha_actual.get():
        entrada_fecha.pack_forget()
    else:
        entrada_fecha.pack(after=check_fecha)
       
# Función para actualizar las categorías según el tipo de transacción
def actualizar_categorias(*args):
    tipo = tipo_var.get()
    if tipo == "Ingreso":
        entrada_categoria['values'] = categorias_ing
        label_tipo_gasto.grid_remove()
        entrada_tipo_gasto.grid_remove()
    elif tipo == "Egreso":
        entrada_categoria['values'] = categorias_eg
        label_tipo_gasto.grid() 
        entrada_tipo_gasto.grid()
    else:
        entrada_categoria['values'] = []
        label_tipo_gasto.grid_remove()
        entrada_tipo_gasto.grid_remove()

# Función para actualizar el tipo de gasto según la categoría seleccionada
def actualizar_tipo_gasto(*args):
    categoria = categoria_var.get()
    if categoria in ["Vivienda", "Prestamo"]:
        tipo_gasto_var.set("Fijo Obligatorio")
    elif categoria in ["Alimentación", "Transporte", "Salud", "Educación", "Internet", "Luz", "Agua", "Gas"]:
        tipo_gasto_var.set("Fijo Necesario")
    elif categoria in ["Entretenimiento", "Viajes", "Otros"]:
        tipo_gasto_var.set("Variable")
    else:
        tipo_gasto_var.set("")


def actualizar_porcentajes():
    distribucion = presupuesto.distribucion_gastos()
    progress_fijo_obligatorio["value"] = distribucion[0] # Fijo Obligatorio
    label_fijo_obligatorio.config(text=f"{distribucion[0]:.1f}%")

    progress_fijo_necesario["value"] = distribucion[1] # Fijo Necesario
    label_fijo_necesario.config(text=f"{distribucion[1]:.1f}%")

    progress_variable["value"] = distribucion[2] # Variable
    label_variable.config(text=f"{distribucion[2]:.1f}%")

    porcentaje_ahorros, porcentaje_saldo = presupuesto.distribucion_ahorros()
    progress_ahorros["value"] = porcentaje_ahorros
    label_ahorros.config(text=f"{porcentaje_ahorros:.1f}%")

    progress_saldo["value"] = porcentaje_saldo
    label_saldo.config(text=f"{porcentaje_saldo:.1f}%")

def monitor_sizes():
    frame1_width = frame_main.winfo_width()
    frame1_height = frame_main.winfo_height()
    frame2_width = frame_statisitcs.winfo_width()
    frame2_height = frame_statisitcs.winfo_height()
    window_width = ventana.winfo_width()
    window_height = ventana.winfo_height()
    print(f"Frame Main Size - Width: {frame1_width}, Height: {frame1_height}")
    print(f"Frame Statistics Size - Width: {frame2_width}, Height: {frame2_height}")
    print(f"Window Size - Width: {window_width}, Height: {window_height}")
    ventana.after(500, monitor_sizes)

# Ventana principal
ventana = tk.Tk()
ventana.title("SIAGEP - Presupuesto Personal")
ventana.minsize(960,700)

# Configuración de la ventana principal
ventana.rowconfigure(0, weight=1)
ventana.columnconfigure(0, weight=3)  # Main frame
ventana.columnconfigure(1, weight=1)  # Right frame

# Frame de entradas
frame_main = ttk.Frame(ventana)
frame_main.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Tipo (ingreso/egreso)
tipo_var = tk.StringVar()
tipo_var.set("Seleccionar")
ttk.Label(frame_main, text="Tipo de transacción:").pack()
ttk.Combobox(frame_main, textvariable=tipo_var, values=["Ingreso", "Egreso"], state="readonly").pack()

#Fecha
ttk.Label(frame_main, text="Fecha (DD-MM-AAAA):").pack()
fecha_actual = tk.BooleanVar()
fecha_actual.set(False)
fecha_actual.trace("w",toggle_entrada_fecha)
check_fecha = ttk.Checkbutton(frame_main, text="Usar fecha actual", variable=fecha_actual) ; check_fecha.pack()
entrada_fecha = ttk.Entry(frame_main)
if not fecha_actual.get():
    entrada_fecha.pack()

#Frame para datos de entrada
frame_inputs = ttk.Frame(frame_main)
frame_inputs.pack(pady=10, padx=10, fill="x")

#Categoría
ttk.Label(frame_inputs, text="Categoría:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
categorias_ing = ["Salario", "Horas extras", "Inversiones", "Otros"]
categorias_eg = ["Vivienda", "Prestamo", "Alimentación", "Transporte", "Salud", "Educación", "Internet", "Luz", "Agua", "Gas", "Entretenimiento", "Viajes", "Otros"]
categoria_var = tk.StringVar()
categoria_var.set("Seleccionar")
entrada_categoria = ttk.Combobox(frame_inputs, textvariable=categoria_var, state="readonly",width=17)
entrada_categoria.grid(row=0, column=1, sticky="e", padx=20, pady=5)
#Vincular la función al cambio de tipo de transacción
tipo_var.trace("w", actualizar_categorias)

# Tipo de Gasto
tipo_gasto_var = tk.StringVar()
tipo_gasto_var.set("")
label_tipo_gasto = ttk.Label(frame_inputs, text="Tipo de gasto:")
label_tipo_gasto.grid(row=0, column=2, sticky="w", padx=5, pady=5)
entrada_tipo_gasto = ttk.Entry(frame_inputs, textvariable=tipo_gasto_var, state="readonly",width=18)
entrada_tipo_gasto.grid(row=0, column=3, sticky="e", padx=20, pady=5)
label_tipo_gasto.grid_remove()
entrada_tipo_gasto.grid_remove()
# Vincular la función al cambio de tipo de transacción y categoría
tipo_var.trace("w", actualizar_categorias)
categoria_var.trace("w", actualizar_tipo_gasto)

# Descripción
ttk.Label(frame_inputs, text="Descripción:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entrada_descripcion = ttk.Entry(frame_inputs,width=18)
entrada_descripcion.grid(row=1, column=1, sticky="e", padx=20, pady=5)

# Monto
ttk.Label(frame_inputs, text="Monto:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entrada_monto = ttk.Entry(frame_inputs,width=18)
entrada_monto.grid(row=2, column=1, sticky="e", padx=20, pady=5)

# Botón para registrar
ttk.Button(frame_main, text="Registrar Movimiento", command=registrar).pack(pady=10)

# Frame ahorros
frame_aportacion = ttk.Frame(frame_main)
frame_aportacion.pack(pady=10, padx=10, fill="x")

# Aportaciones al ahorro
ttk.Label(frame_aportacion, text="Aportaciones al ahorro:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entrada_aportacion = ttk.Entry(frame_aportacion, width=18)
entrada_aportacion.grid(row=0, column=1, sticky="e", padx=5, pady=5)

# Botón para registrar aportación (placed in row=0, column=2)
ttk.Button(frame_aportacion, text="Registrar Aportación", command=registrar_aportacion).grid(row=0, column=2, sticky="w", padx=5, pady=5)

# Descripción de la aportación
ttk.Label(frame_aportacion, text="Descripción:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entrada_descripcion_ahorro = ttk.Entry(frame_aportacion, width=18)
entrada_descripcion_ahorro.grid(row=1, column=1, columnspan=1, sticky="e", padx=5, pady=5)

# Área de resultados
area_resultado = scrolledtext.ScrolledText(frame_main, width=50, height=15)
area_resultado.pack(pady=10, padx=10, fill="both", expand=True)

# Frame derecho (frame_right)
frame_statisitcs = ttk.Frame(ventana)
frame_statisitcs.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Frame para totales
frame_totals = ttk.Frame(frame_statisitcs)
frame_totals.pack(pady=10, padx=10, fill="x")

# Totales
ttk.Label(frame_totals, text="Presupuesto Mensual", font=("Arial", 14, "bold")).pack(pady=10)
label_total_ingresos = ttk.Label(frame_totals, text="Total Ingresos: $0.00")
label_total_ingresos.pack(pady=5)
label_total_egresos = ttk.Label(frame_totals, text="Total de Gastos: $0.00")
label_total_egresos.pack(pady=5)
label_total_ahorros = ttk.Label(frame_totals, text="Aportaciones al Ahorro: $0.00")
label_total_ahorros.pack(pady=5)
label_saldo_actual = ttk.Label(frame_totals, text="Saldo Actual: $0.00")
label_saldo_actual.pack(pady=5)

# Frame para distribución de gastos
frame_percentages = ttk.Frame(frame_statisitcs)
frame_percentages.pack(pady=10, padx=10, fill="x")

# Distribución de gastos
ttk.Label(frame_percentages, text="Distribución de Gastos", font=("Arial", 14, "bold")).pack(pady=5)
style = ttk.Style()
style.configure("Chunky.Horizontal.TProgressbar", barsize=1000,bordercolor='white',thickness=15)

# Fijo Obligatorio
frame_fijo_obligatorio = ttk.Frame(frame_percentages)
frame_fijo_obligatorio.pack(fill="x", pady=5)
ttk.Label(frame_fijo_obligatorio, text="Fijo Obligatorio:").grid(row=0, column=0, sticky="w", padx=5)
progress_fijo_obligatorio = ttk.Progressbar(frame_fijo_obligatorio, orient="horizontal", length=200, mode="determinate", style="Chunky.Horizontal.TProgressbar")
progress_fijo_obligatorio.grid(row=1, column=0, sticky="w", padx=5)
label_fijo_obligatorio = ttk.Label(frame_fijo_obligatorio, text="0%")
label_fijo_obligatorio.grid(row=1, column=1, sticky="w", padx=5)

# Fijo Necesario
frame_fijo_necesario = ttk.Frame(frame_percentages)
frame_fijo_necesario.pack(fill="x", pady=5)
ttk.Label(frame_fijo_necesario, text="Fijo Necesario:").grid(row=0, column=0, sticky="w", padx=5)
progress_fijo_necesario = ttk.Progressbar(frame_fijo_necesario, orient="horizontal", length=200, mode="determinate",style="Chunky.Horizontal.TProgressbar")
progress_fijo_necesario.grid(row=1, column=0, sticky="w", padx=5)
label_fijo_necesario = ttk.Label(frame_fijo_necesario, text="0%")
label_fijo_necesario.grid(row=1, column=1, sticky="w", padx=5)

# Variable
frame_variable = ttk.Frame(frame_percentages)
frame_variable.pack(fill="x", pady=5)
ttk.Label(frame_variable, text="Variable:").grid(row=0, column=0, sticky="w", padx=5)
progress_variable = ttk.Progressbar(frame_variable, orient="horizontal", length=200, mode="determinate",style="Chunky.Horizontal.TProgressbar")
progress_variable.grid(row=1, column=0, sticky="w", padx=5)
label_variable = ttk.Label(frame_variable, text="0%")
label_variable.grid(row=1, column=1, sticky="w", padx=5)

# Distribución de gastos
ttk.Label(frame_percentages, text="Ahorros", font=("Arial", 14, "bold")).pack(pady=5)

# Aportaciones al Ahorro
frame_ahorros = ttk.Frame(frame_percentages)
frame_ahorros.pack(fill="x", pady=5)
ttk.Label(frame_ahorros, text="Aportaciones al Ahorro:").grid(row=0, column=0, sticky="w", padx=5)
progress_ahorros = ttk.Progressbar(frame_ahorros, orient="horizontal", length=200, mode="determinate",style="Chunky.Horizontal.TProgressbar")
progress_ahorros.grid(row=1, column=0, sticky="w", padx=5)
label_ahorros = ttk.Label(frame_ahorros, text="0%")
label_ahorros.grid(row=1, column=1, sticky="w", padx=5)

# Saldo Actual
frame_saldo = ttk.Frame(frame_percentages)
frame_saldo.pack(fill="x", pady=5)
ttk.Label(frame_saldo, text="Saldo Actual:").grid(row=0, column=0, sticky="w", padx=5)
progress_saldo = ttk.Progressbar(frame_saldo, orient="horizontal", length=200, mode="determinate",style="Chunky.Horizontal.TProgressbar")
progress_saldo.grid(row=1, column=0, sticky="w", padx=5)
label_saldo = ttk.Label(frame_saldo, text="0%")
label_saldo.grid(row=1, column=1, sticky="w", padx=5)

# Iniciar
actualizar_resultado()
#monitor_sizes()
ventana.mainloop()