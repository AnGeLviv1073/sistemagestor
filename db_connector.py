import mysql.connector

def conectar_bd(usuario, clave, base_datos):
    try:
        conn = mysql.connector.connect(
            host="192.168.1.65",
            user="admon",
            password="123456",
            database="gestpro1"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
