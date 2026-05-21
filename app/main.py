import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def mostrar_menu():
    print("\n================================================")
    print("     GESTIÓN DE PRÉSTAMO DE LIBROS")
    print("================================================")
    print("1. Carga de datos")
    print("2. Gestión de alumnos")
    print("3. Gestión de préstamos")
    print("4. Listados")
    print("5. Copia de seguridad")
    print("0. Salir")
    print("------------------------------------------------")

def main():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                from carga_datos import menu_carga_datos
                menu_carga_datos()
            elif opcion == 2:
                from alumnos import menu_alumnos
                menu_alumnos()
            elif opcion == 3:
                from prestamos import menu_prestamos
                menu_prestamos()
            elif opcion == 4:
                from listados import menu_listados
                menu_listados()
            elif opcion == 5:
                from backup import menu_backup
                menu_backup()
            elif opcion == 0:
                print("\nAdiós!")
                break
            else:
                print("\nOpción no válida. Inténtalo de nuevo.")
        except ValueError:
            print("\nError: introduce un número.")

if __name__ == "__main__":
    main()