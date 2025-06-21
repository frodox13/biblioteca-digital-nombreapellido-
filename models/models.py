import os
from datetime import datetime
from api.api import descargar_portada_google_books

# Clase Libro que representa un libro en la biblioteca
class Libro:
    def __init__(self, titulo, autor, editorial, anio_publicacion, isbn, disponible=True):
        self.id = 0
        self._titulo = titulo
        self._autor = autor
        self._editorial = editorial
        self._anio_publicacion = anio_publicacion
        self._isbn = isbn
        self._disponible = disponible

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, value):
        self._titulo = value

    def marcar_no_disponible(self):
        self._disponible = False

    def marcar_disponible(self):
        self._disponible = True

    def __str__(self):
        return f"{self._titulo} de {self._autor} ({self._anio_publicacion})"

# Clase Usuario que representa a un usuario de la biblioteca
class Usuario:
    def __init__(self, nombre, email, telefono, tipo_usuario):
        self.id = 0
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.tipo_usuario = tipo_usuario

    def solicitar_prestamo(self, libro, fecha_prestamo, fecha_devolucion):
        if libro._disponible:
            libro.marcar_no_disponible()
            return Prestamo(libro, self, fecha_prestamo, fecha_devolucion)
        else:
            raise Exception("El libro no está disponible para préstamo.")

    def devolver_prestamo(self, prestamo):
        prestamo.devolver()
        prestamo.libro.marcar_disponible()

    def actualizar_datos(self, nombre=None, email=None, telefono=None, tipo_usuario=None):
        if nombre: self.nombre = nombre
        if email: self.email = email
        if telefono: self.telefono = telefono
        if tipo_usuario: self.tipo_usuario = tipo_usuario

#Clase Prestamo que representa un préstamo de un libro a un usuario
class Prestamo:
    def __init__(self, libro, usuario, fecha_prestamo, fecha_devolucion, devuelto=False):
        self.id = 0
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.devuelto = devuelto

    def devolver(self):
        self.fecha_devolucion = datetime.now()
        self.devuelto = True

    def __str__(self):
        return f"Préstamo de '{self.libro.titulo}' a {self.usuario.nombre} ({self.fecha_prestamo})"

#Clase Biblioteca que gestiona los libros, usuarios y préstamos
class Biblioteca:
    def __init__(self):
        self.libros = []
        self.usuarios = []
        self.prestamos = []

    def agregar_libro(self, libro):
        libro.id = len(self.libros) + 1
        self.libros.append(libro)

    def eliminar_libro(self, libro_id):
        self.libros = [libro for libro in self.libros if libro.id != libro_id]

    def registrar_usuario(self, usuario):
        usuario.id = len(self.usuarios) + 1
        self.usuarios.append(usuario)

    def crear_prestamo(self, libro_id, usuario_id, fecha_prestamo, fecha_devolucion):
        libro = next((libro for libro in self.libros if libro.id == libro_id), None)
        usuario = next((usuario for usuario in self.usuarios if usuario.id == usuario_id), None)
        if libro and usuario:
            prestamo = usuario.solicitar_prestamo(libro, fecha_prestamo, fecha_devolucion)
            prestamo.id = len(self.prestamos) + 1
            self.prestamos.append(prestamo)
            return prestamo
        else:
            raise Exception("Libro o usuario no encontrado.")
        
    def buscar_libro_por_titulo(self, titulo):
        return [libro for libro in self.libros if titulo.lower() in libro.titulo.lower()]
    
#Clase apiManager que actúa como intermediario entre la aplicación y la biblioteca 
class apiManager:
    def __init__(self):
        self.biblioteca = Biblioteca()

    def buscar_libro_por_isbn(self, isbn):
        return next((libro for libro in self.biblioteca.libros if libro._isbn == isbn), None)
    
    def descargar_portada_libro(self, isbn):
#Descarga la portada del libro usando la API de Google Books.
#Retorna la ruta local de la imagen descargada.
        try:
            return descargar_portada_google_books(isbn)
        except Exception as e:
            raise e