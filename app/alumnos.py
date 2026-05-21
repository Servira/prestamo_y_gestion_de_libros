import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import conectar, cerrar

def mostrar_menu():
    print("\n================================================")
    print("     GESTIÓN DE ALUMNOS")
    print("================================================")
    print("1. Buscar alumno")
    print("2. Modificar datos de un alumno")
    print("0. Volver al menú principal")
    print("------------------------------------------------")

def buscar_alumno():
    criterio = input("\nIntroduce NIE o nombre del alumno: ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT nie, nombre, apellidos, tramo, bilingue FROM alumnos WHERE nie = %s OR nombre LIKE %s OR apellidos LIKE %s",
                (criterio, f"%{criterio}%", f"%{criterio}%")
            )
            alumnos = cursor.fetchall()
            if alumnos:
                print("\n------------------------------------------------")
                print(f"{'NIE':<12} {'NOMBRE':<20} {'APELLIDOS':<30} {'TRAMO':<8} {'BILINGÜE'}")
                print("------------------------------------------------")
                for a in alumnos:
                    bilingue = "No" if a[4] == 1 else "Sí"
                    tramo = a[3] if a[3] != "0" else "Sin beca"
                    print(f"{a[0]:<12} {a[1]:<20} {a[2]:<30} {tramo:<8} {bilingue}")
            else:
                print("\nNo se encontró ningún alumno.")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def modificar_alumno():
    nie = input("\nIntroduce el NIE del alumno a modificar: ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT nie, nombre, apellidos, tramo, bilingue FROM alumnos WHERE nie = %s", (nie,))
            alumno = cursor.fetchone()
            if not alumno:
                print("\nAlumno no encontrado.")
                return
            print(f"\nDatos actuales:")
            print(f"  Nombre:    {alumno[1]}")
            print(f"  Apellidos: {alumno[2]}")
            print(f"  Tramo:     {alumno[3]}")
            print(f"  Bilingüe:  {'No' if alumno[4] == 1 else 'Sí'}")

            nombre = input(f"\nNuevo nombre [{alumno[1]}]: ") or alumno[1]
            apellidos = input(f"Nuevos apellidos [{alumno[2]}]: ") or alumno[2]
            tramo = input(f"Nuevo tramo (0/I/II) [{alumno[3]}]: ") or alumno[3]
            bilingue = input(f"¿Bilingüe? (s/n) [{'n' if alumno[4] == 1 else 's'}]: ")
            bilingue_val = 0 if bilingue.lower() == "s" else 1

            cursor.execute(
                "UPDATE alumnos SET nombre = %s, apellidos = %s, tramo = %s, bilingue = %s WHERE nie = %s",
                (nombre, apellidos, tramo, bilingue_val, nie)
            )
            conexion.commit()
            print("\nAlumno modificado correctamente.")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def menu_alumnos():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                buscar_alumno()
            elif opcion == 2:
                modificar_alumno()
            elif opcion == 0:
                break
            else:
                print("\nOpción no válida.")
        except ValueError:
            print("\nError: introduce un número.")