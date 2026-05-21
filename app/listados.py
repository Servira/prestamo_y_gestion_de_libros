import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import conectar, cerrar

def mostrar_menu():
    print("\n================================================")
    print("     LISTADOS")
    print("================================================")
    print("1. Listado de alumnos")
    print("2. Listado de libros")
    print("3. Listado de préstamos activos")
    print("4. Listado por curso")
    print("5. Listado por materia")
    print("0. Volver al menú principal")
    print("------------------------------------------------")

def listado_alumnos():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT nie, nombre, apellidos, tramo, bilingue FROM alumnos ORDER BY apellidos")
            alumnos = cursor.fetchall()
            if not alumnos:
                print("\nNo hay alumnos registrados.")
                return
            print("\n------------------------------------------------")
            print(f"{'NIE':<12} {'NOMBRE':<20} {'APELLIDOS':<30} {'TRAMO':<8} {'BILINGÜE'}")
            print("------------------------------------------------")
            for a in alumnos:
                bilingue = "No" if a[4] == 1 else "Sí"
                tramo = a[3] if a[3] != "0" else "Sin beca"
                print(f"{a[0]:<12} {a[1]:<20} {a[2]:<30} {tramo:<8} {bilingue}")
            print(f"\nTotal: {len(alumnos)} alumnos")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def listado_libros():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT l.isbn, l.titulo, l.autor, l.numero_ejemplares, m.nombre, c.nivel FROM libros l JOIN materias m ON l.id_materia = m.id JOIN cursos c ON l.id_curso = c.curso ORDER BY l.titulo"
            )
            libros = cursor.fetchall()
            if not libros:
                print("\nNo hay libros registrados.")
                return
            print("\n------------------------------------------------")
            print(f"{'ISBN':<15} {'TÍTULO':<30} {'AUTOR':<25} {'EJEMP.':<8} {'MATERIA':<20} {'CURSO'}")
            print("------------------------------------------------")
            for l in libros:
                print(f"{l[0]:<15} {l[1]:<30} {l[2]:<25} {l[3]:<8} {l[4]:<20} {l[5]}")
            print(f"\nTotal: {len(libros)} libros")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def listado_prestamos_activos():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT a.nie, al.nombre, al.apellidos, a.isbn, l.titulo, a.fecha_entrega FROM alumnoscursoslibros a JOIN alumnos al ON a.nie = al.nie JOIN libros l ON a.isbn = l.isbn WHERE a.estado = 'P' ORDER BY al.apellidos"
            )
            prestamos = cursor.fetchall()
            if not prestamos:
                print("\nNo hay préstamos activos.")
                return
            print("\n------------------------------------------------")
            print(f"{'NIE':<12} {'ALUMNO':<30} {'ISBN':<15} {'TÍTULO':<30} {'ENTREGA'}")
            print("------------------------------------------------")
            for p in prestamos:
                nombre_completo = f"{p[2]}, {p[1]}"
                print(f"{p[0]:<12} {nombre_completo:<30} {p[3]:<15} {p[4]:<30} {str(p[5])}")
            print(f"\nTotal: {len(prestamos)} préstamos activos")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def listado_por_curso():
    curso = input("\nIntroduce el código del curso (ej: 1ESO-A): ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT nie, nombre, apellidos, tramo FROM alumnos a WHERE EXISTS (SELECT 1 FROM alumnoscursoslibros acl WHERE acl.nie = a.nie AND acl.curso = %s) ORDER BY apellidos",
                (curso,)
            )
            alumnos = cursor.fetchall()
            if not alumnos:
                print(f"\nNo hay alumnos en el curso {curso}.")
                return
            print(f"\n--- ALUMNOS DEL CURSO {curso} ---")
            print(f"{'NIE':<12} {'NOMBRE':<20} {'APELLIDOS':<30} {'TRAMO'}")
            print("------------------------------------------------")
            for a in alumnos:
                tramo = a[3] if a[3] != "0" else "Sin beca"
                print(f"{a[0]:<12} {a[1]:<20} {a[2]:<30} {tramo}")
            print(f"\nTotal: {len(alumnos)} alumnos")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def listado_por_materia():
    materia = input("\nIntroduce el nombre de la materia: ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT l.isbn, l.titulo, l.autor, l.numero_ejemplares, c.nivel FROM libros l JOIN materias m ON l.id_materia = m.id JOIN cursos c ON l.id_curso = c.curso WHERE m.nombre LIKE %s ORDER BY l.titulo",
                (f"%{materia}%",)
            )
            libros = cursor.fetchall()
            if not libros:
                print(f"\nNo hay libros para la materia {materia}.")
                return
            print(f"\n--- LIBROS DE {materia.upper()} ---")
            print(f"{'ISBN':<15} {'TÍTULO':<30} {'AUTOR':<25} {'EJEMP.':<8} {'CURSO'}")
            print("------------------------------------------------")
            for l in libros:
                print(f"{l[0]:<15} {l[1]:<30} {l[2]:<25} {l[3]:<8} {l[4]}")
            print(f"\nTotal: {len(libros)} libros")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def menu_listados():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                listado_alumnos()
            elif opcion == 2:
                listado_libros()
            elif opcion == 3:
                listado_prestamos_activos()
            elif opcion == 4:
                listado_por_curso()
            elif opcion == 5:
                listado_por_materia()
            elif opcion == 0:
                break
            else:
                print("\nOpción no válida.")
        except ValueError:
            print("\nError: introduce un número.")