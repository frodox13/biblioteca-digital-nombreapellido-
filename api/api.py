import requests
import os

def buscar_libro_google_books(titulo):
#Busca libros en Google Books por título y retorna los resultados como lista de diccionarios.
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": titulo, "maxResults": 5}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        libros = []
        for item in data.get("items", []):
            info = item["volumeInfo"]
            libros.append({
                "titulo": info.get("title", ""),
                "autor": ", ".join(info.get("authors", [])),
                "editorial": info.get("publisher", ""),
                "anio_publicacion": info.get("publishedDate", "")[:4],
                "isbn": next((id["identifier"] for id in info.get("industryIdentifiers", []) if id["type"] == "ISBN_13"), ""),
            })
        return libros
    else:
        return []

def registrar_libro_desde_api(libro, db_module):
#Registra un libro obtenido de la API en la base de datos usando el módulo de base de datos.
    db_module.agregar_libro(
        libro["titulo"],
        libro["autor"],
        libro["editorial"],
        int(libro["anio_publicacion"]) if libro["anio_publicacion"].isdigit() else 0,
        libro["isbn"],
        True
    )

def descargar_portada_google_books(isbn, carpeta_destino="portadas"):
# Descarga la portada de un libro desde Google Books usando el ISBN.
# Guarda la imagen en la carpeta especificada y retorna la ruta local.
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": f"isbn:{isbn}"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        if items:
            info = items[0]["volumeInfo"]
            image_links = info.get("imageLinks", {})
            portada_url = image_links.get("thumbnail") or image_links.get("smallThumbnail")
            if portada_url:
                # Crear carpeta si no existe
                os.makedirs(carpeta_destino, exist_ok=True)
                ruta_portada = os.path.join(carpeta_destino, f"{isbn}.jpg")
                # Descargar la imagen
                img_data = requests.get(portada_url).content
                with open(ruta_portada, "wb") as handler:
                    handler.write(img_data)
                return ruta_portada
            else:
                raise FileNotFoundError("No se encontró la portada en Google Books.")
        else:
            raise ValueError("No se encontró el libro con ese ISBN en Google Books.")
    else:
        raise Exception("Error al consultar la API de Google Books.")

