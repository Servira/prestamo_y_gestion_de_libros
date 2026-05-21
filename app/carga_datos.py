import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import conectar, cerrar

def mostrar_menu():
    print("\n================================================")
    print("     CARGA DE DATOS")
    print("================================================")
    print("1. Vaciar base de datos")
    print("2. Cargar alumnos desde CSV (Delphos)")
    print("3. Cargar materias, cursos y libros")
    print("0. Volver al menú principal")
    print("------------------------------------------------")

def vaciar_base_datos():
    confirmar = input("\n¿Estás seguro de que quieres vaciar la base de datos? (s/n): ")
    if confirmar.lower() == "s":
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                cursor.execute("TRUNCATE TABLE alumnoscursoslibros")
                cursor.execute("TRUNCATE TABLE alumnos")
                cursor.execute("TRUNCATE TABLE libros")
                cursor.execute("TRUNCATE TABLE cursos")
                cursor.execute("TRUNCATE TABLE materias")
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                conexion.commit()
                print("\nBase de datos vaciada correctamente.")
            except Exception as e:
                print(f"\nError al vaciar la base de datos: {e}")
            finally:
                cerrar(conexion, cursor)
    else:
        print("\nOperación cancelada.")

def cargar_alumnos_csv():
    ruta = input("\nIntroduce la ruta del fichero CSV: ")
    if not os.path.exists(ruta):
        print("\nError: el fichero no existe.")
        return
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        insertados = 0
        errores = 0
        try:
            with open(ruta, encoding="utf-8") as f:
                for linea in f:
                    campos = linea.strip().split(",")
                    if len(campos) < 18:
                        errores += 1
                        continue
                    alumno = campos[0].strip('"')
                    nie = campos[1].strip('"')
                    matriculado = campos[16].strip('"')
                    tramo_raw = campos[17].strip('"')

                    if matriculado.upper() != "S":
                        continue

                    partes = alumno.split(",")
                    apellidos = partes[0].strip() if len(partes) > 0 else ""
                    nombre = partes[1].strip() if len(partes) > 1 else ""

                    if tramo_raw == "TramoI":
                        tramo = "I"
                    elif tramo_raw == "TramoII":
                        tramo = "II"
                    else:
                        tramo = "0"

                    try:
                        cursor.execute(
                            "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s, %s, %s, %s, %s)",
                            (nie, nombre, apellidos, tramo, 1)
                        )
                        insertados += 1
                    except Exception:
                        errores += 1

            conexion.commit()
            print(f"\nAlumnos insertados: {insertados}")
            print(f"Errores: {errores}")
        except Exception as e:
            print(f"\nError al leer el fichero: {e}")
        finally:
            cerrar(conexion, cursor)

def cargar_materias_cursos_libros():
    print("\n--- CARGAR MATERIA ---")
    nombre_materia = input("Nombre de la materia: ")
    departamento = input("Departamento: ")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO materias (nombre, departamento) VALUES (%s, %s)",
                (nombre_materia, departamento)
            )
            conexion.commit()
            print("Materia añadida correctamente.")

            print("\n--- CARGAR CURSO ---")
            curso = input("Código del curso (ej: 1ESO-A): ")
            nivel = input("Nivel (ej: 1º ESO): ")
            cursor.execute(
                "INSERT INTO cursos (curso, nivel) VALUES (%s, %s)",
                (curso, nivel)
            )
            conexion.commit()
            print("Curso añadido correctamente.")

            print("\n--- CARGAR LIBRO ---")
            isbn = input("ISBN: ")
            titulo = input("Título: ")
            autor = input("Autor: ")
            ejemplares = int(input("Número de ejemplares: "))
            cursor.execute("SELECT id FROM materias WHERE nombre = %s", (nombre_materia,))
            id_materia = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO libros (isbn, titulo, autor, numero_ejemplares, id_materia, id_curso) VALUES (%s, %s, %s, %s, %s, %s)",
                (isbn, titulo, autor, ejemplares, id_materia, curso)
            )
            conexion.commit()
            print("Libro añadido correctamente.")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            cerrar(conexion, cursor)

def menu_carga_datos():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                vaciar_base_datos()
            elif opcion == 2:
                cargar_alumnos_csv()
            elif opcion == 3:
                cargar_materias_cursos_libros()
            elif opcion == 0:
                break
            else:
                print("\nOpción no válida.")
        except ValueError:
            print("\nError: introduce un número.")