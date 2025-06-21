import sqlite3

DB_NAME = "biblioteca.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            editorial TEXT,
            anio_publicacion INTEGER,
            isbn TEXT,
            disponible INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            email TEXT,
            telefono TEXT,
            tipo_usuario TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER,
            usuario_id INTEGER,
            fecha_prestamo TEXT,
            fecha_devolucion TEXT,
            devuelto INTEGER,
            FOREIGN KEY(libro_id) REFERENCES libros(id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    """)
    conn.commit()
    conn.close()

# Base de datos SQLite
def connect_db():

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    # Tabla libro
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editorial TEXT NOT NULL,
            anio_publicacion INTEGER NOT NULL,
            isbn TEXT NOT NULL UNIQUE,
            disponible BOOLEAN NOT NULL DEFAULT 1
        )
    ''')
    # Tabla usuario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefono TEXT,
            tipo_usuario TEXT
        )
    ''')
    # Tabla prestamo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prestamo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            fecha_prestamo DATE NOT NULL,
            fecha_devolucion DATE,
            devuelto INTEGER DEFAULT 0,
            FOREIGN KEY (libro_id) REFERENCES libro(id),
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        )
    ''')
    conn.commit()
    conn.close()


# CRUD para LIBRO
def agregar_libro(titulo, autor, editorial, anio_publicacion, isbn, disponible=True):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO libro (titulo, autor, editorial, anio_publicacion, isbn, disponible)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (titulo, autor, editorial, anio_publicacion, isbn, int(disponible)))
    conn.commit()
    conn.close()

def obtener_libros():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM libro')
    libros = cursor.fetchall()
    conn.close()
    return libros

def actualizar_libro(id, titulo, autor, editorial, anio_publicacion, isbn, disponible):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE libro SET titulo=?, autor=?, editorial=?, anio_publicacion=?, isbn=?, disponible=?
        WHERE id=?
    ''', (titulo, autor, editorial, anio_publicacion, isbn, int(disponible), id))
    conn.commit()
    conn.close()

def eliminar_libro(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM libro WHERE id=?', (id,))
    conn.commit()
    conn.close()

def obtener_libro_por_id(libro_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM libro WHERE id=?', (libro_id,))
    libro = cursor.fetchone()
    conn.close()
    if libro:
        # Retorna un diccionario para facilitar el acceso por nombre
        return {
            'id': libro[0],
            'titulo': libro[1],
            'autor': libro[2],
            'editorial': libro[3],
            'anio_publicacion': libro[4],
            'isbn': libro[5],
            'disponible': bool(libro[6])
        }
    return None

# CRUD para USUARIO
def agregar_usuario(nombre, email, telefono, tipo_usuario):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuario (nombre, email, telefono, tipo_usuario)
        VALUES (?, ?, ?, ?)
    ''', (nombre, email, telefono, tipo_usuario))
    conn.commit()
    conn.close()

def obtener_usuarios():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuario')
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def eliminar_usuario(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuario WHERE id=?', (id,))
    conn.commit()
    conn.close()

# CRUD para PRESTAMO
def agregar_prestamo(libro_id, usuario_id, fecha_prestamo, fecha_devolucion=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prestamo (libro_id, usuario_id, fecha_prestamo, fecha_devolucion)
        VALUES (?, ?, ?, ?)
    ''', (libro_id, usuario_id, fecha_prestamo, fecha_devolucion))
    conn.commit()
    conn.close()

def obtener_prestamos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prestamo')
    prestamos = cursor.fetchall()
    conn.close()
    return prestamos

def eliminar_prestamo(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM prestamo WHERE id=?', (id,))
    conn.commit()
    conn.close()

def obtener_prestamo_por_id(prestamo_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prestamo WHERE id=?', (prestamo_id,))
    prestamo = cursor.fetchone()
    conn.close()
    if prestamo:
        return {
            'id': prestamo[0],
            'libro_id': prestamo[1],
            'usuario_id': prestamo[2],
            'fecha_prestamo': prestamo[3],
            'fecha_devolucion': prestamo[4],
            'devuelto': bool(prestamo[5])
        }
    return None

def devolver_prestamo(prestamo_id, fecha_devolucion):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE prestamo
        SET fecha_devolucion = ?, devuelto = 1
        WHERE id = ?
    ''', (fecha_devolucion, prestamo_id))
    conn.commit()
    conn.close()