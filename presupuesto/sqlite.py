import sqlite3 as sq3

def conection():
    return sq3.connect('data/siagep.db')

def create_database():
    connexion = conection()
    cursor = connexion.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS transacciones(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        categoria TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        monto REAL NOT NULL,
        fecha TEXT NOT NULL,
        tipo_gasto TEXT
        )
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS ahorros(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL DEFAULT 'Ahorro',
        descripcion TEXT NOT NULL,
        monto REAL NOT NULL,
        fecha TEXT NOT NULL
        )
        '''
    )   
    connexion.commit()
    connexion.close()

def insertar_transaccion(tipo, categoria, descripcion, monto, fecha, tipo_gasto):
    conexion = conection()
    cursor = conexion.cursor()
    cursor.execute(
        '''
        INSERT INTO transacciones (tipo, categoria, descripcion, monto, fecha, tipo_gasto) VALUES (?, ?, ?, ?, ?, ?)
        ''', (tipo, categoria, descripcion, monto, fecha, tipo_gasto)
    )
    conexion.commit()
    conexion.close()

def obtener_transacciones():
    conexion = conection()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM transacciones')
    transacciones = cursor.fetchall()
    conexion.close()
    return transacciones if transacciones else []

def insertar_ahorro(tipo, descripcion, monto, fecha):
    conexion = conection()
    cursor = conexion.cursor()
    cursor.execute(
        '''
        INSERT INTO ahorros (tipo, descripcion, monto, fecha) VALUES (?, ?, ?, ?)
        ''', (tipo, descripcion, monto, fecha)
    )
    conexion.commit()
    conexion.close()

def obtener_ahorros():
    conexion = conection()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM ahorros')
    ahorros = cursor.fetchall()
    conexion.close()
    return ahorros if ahorros else []

#
# create_database()