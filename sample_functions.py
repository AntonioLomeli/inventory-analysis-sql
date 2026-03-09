import tkinter as tk
import pandas as pd
import sqlite3 as sql
from tkinter import ttk
from tkinter import messagebox
from os import path
   
def validar_fecha(dia,mes,an):
    validacion = False
    
    if dia.isnumeric() and mes.isnumeric() and an.isnumeric() and len(dia)==2 and len(mes)==2:
        
        if int(dia)>=1 and int(dia)<=31 and int(mes)>=1 and int(mes)<=12 and len(an)==4:
            validacion = True
        else:
            messagebox.showerror('Error en las fechas', 'Las fechas son incorrectas, asegúrate haber ingresado correctamente el día, mes y año')
    else:
        messagebox.showerror('Error en las fechas', 'Las fechas son incorrectas, asegúrate haber ingresado correctamente el día, mes y año')
        
    return validacion

def btn_enter(event, btn):
    btn.config(bg="red", fg = "white")

def btn_leave(event, btn):
    btn.config(bg="#ED7F28", fg = "white")

def conectar_db():
    carpeta = path.dirname(__file__)
    direccion = path.join(carpeta, 'Operacional_DB.db')
    return sql.connect(direccion)

def sql_crear_orden(tipo, ID_movimiento, fecha, suc_origen, suc_destino = None, id_cliente = None, ID_chofer = None, Completo = None, Atiempo = None):
    conn = conectar_db()
    if tipo == 'Traspaso':
        command = "INSERT INTO Traspaso (ID_Traspaso, Fecha, Origen, Destino, ID_Chofer, Completo, A_Tiempo) VALUES(?,?,?,?,?,?,?)"
        values = (ID_movimiento, fecha, suc_origen, suc_destino, ID_chofer, Completo, Atiempo)
    elif tipo == 'Salida':
        command = "INSERT INTO Salidas (ID_Salida, Fecha, ID_Cliente, ID_Sucursal, Completo, A_Tiempo, Tipo) VALUES(?,?,?,?,?,?, NULL)"
        values = (ID_movimiento, fecha, id_cliente, suc_origen, Completo, Atiempo)
    elif tipo == 'Produccion':
        command = "INSERT INTO Produccion (ID_Produccion, Fecha, Planta) VALUES(?,?,?)"
        values = (ID_movimiento, fecha, suc_origen)
    
    conn.execute(command, values)
    conn.commit()
    conn.close()
    messagebox.showinfo('Orden Creada Exitosamente!', "La orden se ha creado exitosamente")

def obtener_clientes():
    conn = conectar_db()
    consulta = "SELECT ID_Cliente, Nombre, Localidad FROM Clientes"
    
    df = pd.read_sql_query(consulta, conn)
    df['Nombre'] = df['Nombre'].apply(concatenar)
    df['Localidad'] = df['Localidad'].apply(concatenar)
    conn.close()
    
    return df

def concatenar(columna):
        return '_'.join(columna.split())

def obtener_productos ( ): # Regresa un DataFrame
    
    conn = conectar_db()
    consulta = "SELECT prod.ID_Producto, " \
                "prod.Nombre, prov.Nombre As Proveedor " \
                "FROM Productos prod INNER JOIN Proveedores prov ON prod.ID_Proveedor = prov.ID_Proveedor;"
    
    df = pd.read_sql_query(consulta, conn)
    df['Nombre'] = df['Nombre'].apply(concatenar)
    df['Proveedor'] = df['Proveedor'].apply(concatenar)
    conn.close()
    
    return df

def obtener_sucursales () -> pd.DataFrame: 
    
    conn = conectar_db()
    consulta = "SELECT ID_Sucursal, Nombre FROM Sucursales"
    
    df = pd.read_sql_query(consulta, conn)
    df['Nombre'] = df['Nombre'].apply(concatenar)
    
    conn.close()
    
    return df

def obtener_empleados():
    conn = conectar_db()
    consulta = "SELECT ID_Chofer, Nombre FROM Choferes"
    
    df = pd.read_sql_query(consulta, conn)
    df['Nombre'] = df['Nombre'].apply(concatenar)
    
    conn.close()
    
    return df    

def buscar_productos(event, 
                     datos: pd.DataFrame, 
                     cbb: tk.ttk.Combobox) -> pd.DataFrame: 
    caracter = cbb.get() 
    cbb.delete(0, tk.END)

    if caracter.isnumeric():
        caracter  = str(caracter)
        resultado = datos[datos['ID_Producto'].astype(str).str.contains(caracter, case=False)]
    else:
        resultado = datos[datos['Nombre'].str.contains(caracter, case=False)]
        
    
    cbb['values'] = resultado[['ID_Producto','Nombre','Proveedor']].values.tolist()

