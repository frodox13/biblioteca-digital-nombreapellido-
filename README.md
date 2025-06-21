# Biblioteca Digital

Este proyecto es una **Biblioteca Digital** desarrollada en Python, que permite gestionar libros, usuarios y préstamos, además de buscar libros en la API pública de Google Books.

## Descripción

La aplicación permite:
- Registrar, consultar, actualizar y eliminar libros y usuarios.
- Crear y devolver préstamos de libros.
- Consultar el listado de libros, usuarios y préstamos.
- Buscar libros en Google Books y agregarlos a la base de datos local.
- Todo el sistema utiliza una base de datos SQLite para persistencia.

## Estructura del Proyecto

```
.
├── main.py                # Archivo principal de la aplicación
├── models.py              # Definición de modelos, sus atributos y metodos
├── database.py            # Base de datos de la aplicación
├── views.py               # Lógica de presentación y manejo de la interfaz de usuario
├── controllers.py         # Controladores para la interacción entre modelos y vistas
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación del proyecto
```

## Instalación y Uso

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/biblioteca_digital.git
   ```
2. Navegar al directorio del proyecto:
   ```bash
   cd biblioteca_digital
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar la aplicación:
   ```bash
   python biblioteca.py
   ```


