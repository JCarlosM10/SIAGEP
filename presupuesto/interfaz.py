from presupuesto.operaciones import agregar_transaccion, mostrar_resumen
from presupuesto.persistencia import guardar_presupuesto, cargar_presupuesto

def menu_principal():
    print("\n--- SIAGEP - Gestión de Presupuesto Personal ---")
    print("1. Agregar ingreso")
    print("2. Agregar egreso")
    print("3. Ver resumen")
    print("4. Guardar y salir")
    return input("Selecciona una opción: ")

def pedir_datos_transaccion(tipo):
    categoria = input(f"Ingrese la categoría del {tipo} (ej. salario, renta, comida): ")
    while True:
        try:
            monto = float(input(f"Ingrese el monto del {tipo}: "))
            break
        except ValueError:
            print("Por favor, ingresa un número válido.")
    return categoria, monto

def iniciar_interfaz():
    presupuesto = cargar_presupuesto()

    while True:
        opcion = menu_principal()

        if opcion == "1":
            categoria, monto = pedir_datos_transaccion("ingreso")
            agregar_transaccion(presupuesto, "ingreso", categoria, monto)
            print("✅ Ingreso registrado.")
        
        elif opcion == "2":
            categoria, monto = pedir_datos_transaccion("egreso")
            agregar_transaccion(presupuesto, "egreso", categoria, monto)
            print("✅ Egreso registrado.")
        
        elif opcion == "3":
            mostrar_resumen(presupuesto)

        elif opcion == "4":
            guardar_presupuesto(presupuesto)
            print("¡Hasta la próxima!")
            break
        else:
            print("Opción no válida, intenta nuevamente.")
