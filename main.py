from controllers import controllers as ctrl
from api import api
import database.database as db

def es_nombre_valido(nombre):
    return nombre.replace(" ", "").isalpha()

def es_str_sin_numero(texto):
    return texto.replace(" ", "").isalpha()

def pedir_int(mensaje):
    while True:
        valor = input(mensaje)
        if valor.isdigit():
            return int(valor)
        print("Error: Debe ingresar un número entero.")

def main():
    db.create_tables()
    while True:
        print("\n--- Biblioteca Digital ---")
        print("1. Registrar libro")
        print("2. Registrar usuario")
        print("3. Crear préstamo")
        print("4. Devolver libro")
        print("5. Ver libros")
        print("6. Ver usuarios")
        print("7. Ver préstamos")
        print("8. Buscar libro en Google Books")
        print("9. Descargar portada de libro")
        print("10. Eliminar libro")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                titulo = input("Título: ")
                autor = input("Autor: ")
                if not es_str_sin_numero(autor):
                    raise ValueError("El autor no puede contener números.")
                editorial = input("Editorial: ")
                anio = pedir_int("Año de publicación: ")
                isbn = input("ISBN: ")
                ctrl.registrar_libro(titulo, autor, editorial, anio, isbn)
                print("Libro registrado.")

            elif opcion == "2":
                nombre = input("Nombre: ")
                if not es_nombre_valido(nombre):
                    raise ValueError("El nombre no puede contener números ni caracteres especiales.")
                email = input("Email: ")
                telefono = input("Teléfono: ")
                tipo = input("Tipo de usuario: ")
                ctrl.registrar_usuario(nombre, email, telefono, tipo)
                print("Usuario registrado.")

            elif opcion == "3":
                libro_id = pedir_int("ID del libro: ")
                usuario_id = pedir_int("ID del usuario: ")
                fecha_prestamo = input("Fecha de préstamo (YYYY-MM-DD): ")
                if ctrl.crear_prestamo(libro_id, usuario_id, fecha_prestamo):
                    print("Préstamo creado.")
                else:
                    print("No se pudo crear el préstamo (libro no disponible o datos incorrectos).")

            elif opcion == "4":
                prestamo_id = pedir_int("ID del préstamo: ")
                if ctrl.devolver_prestamo(prestamo_id):
                    print("Libro devuelto.")
                else:
                    print("No se pudo devolver el libro (ID incorrecto o ya devuelto).")

            elif opcion == "5":
                libros = ctrl.obtener_libros()
                if libros:
                    for libro in libros:
                        print(f"ID: {libro[0]}, Título: {libro[1]}, Autor: {libro[2]}, Editorial: {libro[3]}, Año: {libro[4]}, ISBN: {libro[5]}, Disponible: {'Sí' if libro[6] else 'No'}")
                else:
                    print("No hay libros registrados.")

            elif opcion == "6":
                usuarios = ctrl.obtener_usuarios()
                if usuarios:
                    for usuario in usuarios:
                        print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Email: {usuario[2]}, Teléfono: {usuario[3]}, Tipo: {usuario[4]}")
                else:
                    print("No hay usuarios registrados.")

            elif opcion == "7":
                prestamos = ctrl.obtener_prestamos()
                if prestamos:
                    for prestamo in prestamos:
                        print(f"ID: {prestamo[0]}, Libro ID: {prestamo[1]}, Usuario ID: {prestamo[2]}, Fecha préstamo: {prestamo[3]}, Fecha devolución: {prestamo[4]}, Devuelto: {'Sí' if prestamo[5] else 'No'}")
                else:
                    print("No hay préstamos registrados.")

            elif opcion == "8":
                titulo = input("Título a buscar: ")
                resultados = api.buscar_libro_google_books(titulo)
                for idx, libro in enumerate(resultados, 1):
                    print(f"{idx}. {libro}")
                if resultados:
                    guardar = input("¿Desea registrar alguno en la base de datos? (s/n): ")
                    if guardar.lower() == "s":
                        num = pedir_int("Número del libro a registrar: ")
                        if 1 <= num <= len(resultados):
                            api.registrar_libro_desde_api(resultados[num-1], db)
                            print("Libro registrado desde Google Books.")
                        else:
                            print("Número fuera de rango.")

            elif opcion == "9":
                isbn = input("Ingrese el ISBN del libro: ")
                try:
                    ruta = api.descargar_portada_google_books(isbn)
                    print(f"Portada descargada en: {ruta}")
                except Exception as e:
                    print(f"Error al descargar portada: {e}")

            elif opcion == "10":
                libro_id = pedir_int("Ingrese el ID del libro a eliminar: ")
                libro = db.obtener_libro_por_id(libro_id)
                if libro:
                    try:
                        ctrl.eliminar_libro(libro_id)
                        print("Libro eliminado correctamente.")
                    except Exception as e:
                        print(f"Error al eliminar libro: {e}")
                else:
                    print("Ese libro no existe. Vuelve a probar con una ID existente.")

            elif opcion == "0":
                print("¡Hasta luego!")
                break

            else:
                print("Opción no válida.")

        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()