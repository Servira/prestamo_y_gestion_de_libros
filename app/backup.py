import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import csv
from datetime import date
from db import conectar, cerrar

def mostrar_menu():
    print("\n================================================")
    print("     COPIA DE SEGURIDAD")
    print("================================================")
    print("1. Exportar todos los datos en SQL")
    print("2. Exportar todos los datos en CSV")
    print("3. Exportar todos los datos en JSON")
    print("0. Volver al menú principal")
    print("------------------------------------------------")

def obtener_datos_tablas(cursor):
    tablas = ["materias", "cursos", "libros", "alumnos", "alumnoscursoslibros"]
    datos = {}
    for tabla in tablas:
        cursor.execute(f"SELECT * FROM {tabla}")
        columnas = [desc[0] for desc in cursor.description]
        filas = cursor.fetchall()
        datos[tabla] = {"columnas": columnas, "filas": filas}
    return datos

def exportar_sql():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            datos = obtener_datos_tablas(cursor)
            nombre = f"backup_{date.today()}.sql"
            with open(nombre, "w", encoding="utf-8") as f:
                f.write(f"-- Backup generado el {date.today()}\n\n")
                for tabla, contenido in datos.items():
                    f.write(f"-- Tabla: {tabla}\n")
                    f.write(f"TRUNCATE TABLE {tabla};\n")
                    for fila in contenido["filas"]:
                        valores = ", ".join(
                            f"'{str(v)}'" if v is not None else "NULL"
                            for v in fila
                        )
                        f.write(f"INSERT INTO {tabla} VALUES ({valores});\n")
                    f.write("\n")
            print(f"\nBackup SQL generado: {nombre}")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def exportar_csv():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            datos = obtener_datos_tablas(cursor)
            nombre = f"backup_{date.today()}.csv"
            with open(nombre, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for tabla, contenido in datos.items():
                    writer.writerow([f"### {tabla} ###"])
                    writer.writerow(contenido["columnas"])
                    for fila in contenido["filas"]:
                        writer.writerow(fila)
                    writer.writerow([])
            print(f"\nBackup CSV generado: {nombre}")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def exportar_json():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            datos = obtener_datos_tablas(cursor)
            nombre = f"backup_{date.today()}.json"
            resultado = {}
            for tabla, contenido in datos.items():
                resultado[tabla] = [
                    dict(zip(contenido["columnas"], fila))
                    for fila in contenido["filas"]
                ]
            with open(nombre, "w", encoding="utf-8") as f:
                json.dump(resultado, f, ensure_ascii=False, indent=2, default=str)
            print(f"\nBackup JSON generado: {nombre}")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def menu_backup():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                exportar_sql()
            elif opcion == 2:
                exportar_csv()
            elif opcion == 3:
                exportar_json()
            elif opcion == 0:
                break
            else:
                print("\nOpción no válida.")
        except ValueError:
            print("\nError: introduce un número.")