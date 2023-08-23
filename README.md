# Aplicación FastAPI con README en Markdown

Puedes utilizar este contenido en Markdown para el README de tu aplicación FastAPI en GitHub.

## Aplicación Python FastAPI

Esta es una aplicación Python FastAPI que proporciona una API para gestionar libros, usuarios y autores en un sistema de biblioteca.

### Requisitos previos

- Python 3.x
- [FastAPI](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
- [SQLite](https://www.sqlite.org/index.html)

### Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/luisqpra/FastApiBooks.git
   cd FastApiBooks
   ```

2. Crea un entorno virtual y actívalo:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala los paquetes necesarios:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   uvicorn main:app --reload
   ```

Accede a la documentación de la API visitando `http://127.0.0.1:8000/docs` en tu navegador web.

## Puntos finales de la API

La API ofrece puntos finales para gestionar usuarios, libros y autores. Aquí tienes algunos puntos finales disponibles:

- `GET /` - Pagina inicial "Hello word"
- `POST /user/new` - Crear un nuevo usuario
- `GET /users` - Mostrar todos los usuarios
- `GET /user/details` - Mostrar detalles de un usuario
- `PUT /user/update` - Actualizar un usuario
- `DELETE /user/delete` - Eliminar un usuario
- `POST /book/new` - Crear un nuevo libro
- `GET /books` - Mostrar todos los libros
- `GET /book/details` - Mostrar detalles de un libro
- `PUT /book/update` - Actualizar un libro
- `DELETE /book/delete` - Eliminar un libro
- `POST /author/new` - Crear un nuevo autor

## Contribuciones

Si deseas contribuir a este proyecto, no dudes en hacer un fork del repositorio y enviar una solicitud de extracción.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.