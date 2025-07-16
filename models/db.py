# models/db.py
import mysql.connector
from config import DB_CONFIG

def conectar():
    return mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "",
        database= "turnero_estetica"
    )
