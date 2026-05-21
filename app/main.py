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
                print("\n[Carga de datos - próximamente]")
            elif opcion == 2:
                print("\n[Gestión de alumnos - próximamente]")
            elif opcion == 3:
                print("\n[Gestión de préstamos - próximamente]")
            elif opcion == 4:
                print("\n[Listados - próximamente]")
            elif opcion == 5:
                print("\n[Copia de seguridad - próximamente]")
            elif opcion == 0:
                print("\nAdiós!")
                break
            else:
                print("\nOpción no válida. Inténtalo de nuevo.")
        except ValueError:
            print("\nError: introduce un número.")

if __name__ == "__main__":
    main()