from models.models import Libro, Usuario, Prestamo
import database.database as db
from datetime import datetime

# ---------------------------
# Controlador de Libros
# ---------------------------

def registrar_libro(titulo, autor, editorial, anio_publicacion, isbn, disponible=True):
    """Registra un libro en la base de datos."""
    db.agregar_libro(titulo, autor, editorial, anio_publicacion, isbn, disponible)

def obtener_libros():
    """Obtiene todos los libros de la base de datos."""
    return db.obtener_libros()

def actualizar_libro(id, titulo, autor, editorial, anio_publicacion, isbn, disponible):
    """Actualiza los datos de un libro."""
    db.actualizar_libro(id, titulo, autor, editorial, anio_publicacion, isbn, disponible)

def eliminar_libro(id):
    """Elimina un libro por su ID."""
    db.eliminar_libro(id)

# ---------------------------
# Controlador de Usuarios
# ---------------------------

def registrar_usuario(nombre, email, telefono, tipo_usuario):
    """Registra un usuario en la base de datos."""
    db.agregar_usuario(nombre, email, telefono, tipo_usuario)

def obtener_usuarios():
    """Obtiene todos los usuarios de la base de datos."""
    return db.obtener_usuarios()

def eliminar_usuario(id):
    """Elimina un usuario por su ID."""
    db.eliminar_usuario(id)

# ---------------------------
# Controlador de Préstamos
# ---------------------------

def crear_prestamo(libro_id, usuario_id, fecha_prestamo, fecha_devolucion=None):
    """Crea un préstamo si el libro está disponible."""
    libro = db.obtener_libro_por_id(libro_id)
    if libro and libro['disponible']:
        db.agregar_prestamo(libro_id, usuario_id, fecha_prestamo, fecha_devolucion)
        db.actualizar_libro(libro_id, libro['titulo'], libro['autor'], libro['editorial'], libro['anio_publicacion'], libro['isbn'], False)
        return True
    return False

def devolver_prestamo(prestamo_id):
    """Marca un préstamo como devuelto y actualiza el libro como disponible."""
    prestamo = db.obtener_prestamo_por_id(prestamo_id)
    if prestamo and not prestamo['devuelto']:
        fecha_devolucion = datetime.now().strftime("%Y-%m-%d")
        db.devolver_prestamo(prestamo_id, fecha_devolucion)
        libro = db.obtener_libro_por_id(prestamo['libro_id'])
        db.actualizar_libro(libro['id'], libro['titulo'], libro['autor'], libro['editorial'], libro['anio_publicacion'], libro['isbn'], True)
        return True
    return False

def obtener_prestamos():
    """Obtiene todos los préstamos de la base de datos."""
    return db.obtener_prestamos()