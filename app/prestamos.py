import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from datetime import date
from db import conectar, cerrar

def mostrar_menu():
    print("\n================================================")
    print("     GESTIÓN DE PRÉSTAMOS")
    print("================================================")
    print("1. Asignar libros a un alumno")
    print("2. Registrar devolución de libros")
    print("3. Cerrar préstamo")
    print("4. Ver préstamos de un alumno")
    print("5. Generar contrato de préstamo")
    print("0. Volver al menú principal")
    print("------------------------------------------------")

def asignar_libros():
    nie = input("\nIntroduce el NIE del alumno: ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT nombre, apellidos FROM alumnos WHERE nie = %s", (nie,))
            alumno = cursor.fetchone()
            if not alumno:
                print("\nAlumno no encontrado.")
                return
            print(f"\nAlumno: {alumno[1]}, {alumno[0]}")

            curso = input("Introduce el código del curso (ej: 1ESO-A): ")
            cursor.execute(
                "SELECT l.isbn, l.titulo, l.autor, l.numero_ejemplares FROM libros l WHERE l.id_curso = %s",
                (curso,)
            )
            libros = cursor.fetchall()
            if not libros:
                print("\nNo hay libros para ese curso.")
                return

            print("\n--- LIBROS DISPONIBLES ---")
            for i, l in enumerate(libros, 1):
                print(f"{i}. [{l[0]}] {l[1]} - {l[2]} (Ejemplares: {l[3]})")

            seleccion = input("\nIntroduce los números de los libros a asignar separados por comas: ")
            indices = [int(x.strip()) - 1 for x in seleccion.split(",")]

            for i in indices:
                if 0 <= i < len(libros):
                    isbn = libros[i][0]
                    try:
                        cursor.execute(
                            "INSERT INTO alumnoscursoslibros (nie, curso, isbn, fecha_entrega, estado) VALUES (%s, %s, %s, %s, %s)",
                            (nie, curso, isbn, date.today(), "P")
                        )
                        print(f"Libro [{isbn}] asignado correctamente.")
                    except Exception as e:
                        print(f"Error al asignar libro [{isbn}]: {e}")

            conexion.commit()
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def registrar_devolucion():
    nie = input("\nIntroduce el NIE del alumno: ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT a.isbn, l.titulo, a.fecha_entrega FROM alumnoscursoslibros a JOIN libros l ON a.isbn = l.isbn WHERE a.nie = %s AND a.estado = 'P'",
                (nie,)
            )
            prestamos = cursor.fetchall()
            if not prestamos:
                print("\nEste alumno no tiene préstamos activos.")
                return

            print("\n--- PRÉSTAMOS ACTIVOS ---")
            for i, p in enumerate(prestamos, 1):
                print(f"{i}. [{p[0]}] {p[1]} - Entregado: {p[2]}")

            seleccion = input("\nIntroduce los números de los libros devueltos separados por comas: ")
            indices = [int(x.strip()) - 1 for x in seleccion.split(",")]

            for i in indices:
                if 0 <= i < len(prestamos):
                    isbn = prestamos[i][0]
                    cursor.execute(
                        "UPDATE alumnoscursoslibros SET estado = 'D', fecha_devolucion = %s WHERE nie = %s AND isbn = %s",
                        (date.today(), nie, isbn)
                    )
                    print(f"Libro [{isbn}] devuelto correctamente.")

            conexion.commit()
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def cerrar_prestamo():
    nie = input("\nIntroduce el NIE del alumno: ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM alumnoscursoslibros WHERE nie = %s AND estado = 'P'",
                (nie,)
            )
            pendientes = cursor.fetchone()[0]
            if pendientes > 0:
                print(f"\nEl alumno todavía tiene {pendientes} libro(s) sin devolver.")
                return
            print("\nTodos los libros han sido devueltos. Préstamo cerrado correctamente.")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def ver_prestamos():
    nie = input("\nIntroduce el NIE del alumno: ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT a.isbn, l.titulo, a.fecha_entrega, a.fecha_devolucion, a.estado FROM alumnoscursoslibros a JOIN libros l ON a.isbn = l.isbn WHERE a.nie = %s",
                (nie,)
            )
            prestamos = cursor.fetchall()
            if not prestamos:
                print("\nEste alumno no tiene préstamos registrados.")
                return
            print("\n------------------------------------------------")
            print(f"{'ISBN':<15} {'TÍTULO':<30} {'ENTREGA':<12} {'DEVOLUCIÓN':<12} {'ESTADO'}")
            print("------------------------------------------------")
            for p in prestamos:
                estado = "Prestado" if p[4] == "P" else "Devuelto"
                devolucion = str(p[3]) if p[3] else "-"
                print(f"{p[0]:<15} {p[1]:<30} {str(p[2]):<12} {devolucion:<12} {estado}")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def generar_contrato():
    nie = input("\nIntroduce el NIE del alumno: ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT nombre, apellidos FROM alumnos WHERE nie = %s", (nie,))
            alumno = cursor.fetchone()
            if not alumno:
                print("\nAlumno no encontrado.")
                return

            cursor.execute(
                "SELECT l.titulo, l.autor, a.isbn, a.fecha_entrega FROM alumnoscursoslibros a JOIN libros l ON a.isbn = l.isbn WHERE a.nie = %s AND a.estado = 'P'",
                (nie,)
            )
            prestamos = cursor.fetchall()
            if not prestamos:
                print("\nEste alumno no tiene préstamos activos.")
                return

            nombre_fichero = f"contrato_{nie}_{date.today()}.txt"
            with open(nombre_fichero, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("    CONTRATO DE PRÉSTAMO DE LIBROS\n")
                f.write("    IES Arcipreste de Hita\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Fecha: {date.today()}\n\n")
                f.write(f"Alumno: {alumno[1]}, {alumno[0]}\n")
                f.write(f"NIE: {nie}\n\n")
                f.write("Libros prestados:\n")
                f.write("-" * 60 + "\n")
                for i, p in enumerate(prestamos, 1):
                    f.write(f"{i}. {p[0]} - {p[1]}\n")
                    f.write(f"   ISBN: {p[2]} | Fecha entrega: {p[3]}\n")
                f.write("-" * 60 + "\n\n")
                f.write("El alumno/a se compromete a devolver los libros\n")
                f.write("en buen estado al finalizar el curso escolar.\n\n")
                f.write("Firma del alumno/tutor:\n\n")
                f.write("_______________________________\n\n")
                f.write("Firma del responsable del centro:\n\n")
                f.write("_______________________________\n")

            print(f"\nContrato generado: {nombre_fichero}")
            firmado = input("¿El contrato ha sido firmado? (s/n): ")
            if firmado.lower() == "s":
                print("Contrato registrado como firmado.")
            else:
                print("Contrato pendiente de firma.")

        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def menu_prestamos():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                asignar_libros()
            elif opcion == 2:
                registrar_devolucion()
            elif opcion == 3:
                cerrar_prestamo()
            elif opcion == 4:
                ver_prestamos()
            elif opcion == 5:
                generar_contrato()
            elif opcion == 0:
                break
            else:
                print("\nOpción no válida.")
        except ValueError:
            print("\nError: introduce un número.")