# API REST para un Mini-Blog

Este proyecto es el backend para un sistema de mini-blog que permite a los usuarios registrarse, crear publicaciones y comentar en las publicaciones de otros, construido con FastAPI y SQLAlchemy asíncrono.

## Stack Tecnológico

*   **Lenguaje:** Python 3.9+
*   **Framework:** FastAPI
*   **ORM:** SQLAlchemy 2.0 (con soporte `async`)
*   **Validación de Datos:** Pydantic
*   **Base de Datos:** PostgreSQL
*   **Gestión de Dependencias:** Poetry
*   **Migraciones:** Alembic
*   **Pruebas:** Pytest
*   **Contenerización:** Docker & Docker Compose

## Fase 1: Diseño y Modelado de la Base de Datos

### Diagrama Entidad-Relación (E/R)

A continuación se muestra el diagrama E/R que representa la estructura de la base de datos del proyecto.

![Diagrama E/R](docs/Diagrama.jpg)

### Diseño de Entidades y Relaciones

La base de datos se compone de tres tablas principales diseñadas para almacenar la información de los usuarios, sus publicaciones y los comentarios asociados.

#### **Tabla `users`**
Almacena la información de los usuarios registrados en el sistema.
-   `id` (BIGINT, Clave Primaria): Identificador único para cada usuario.
-   `username` (VARCHAR, Único): Nombre de usuario único.
-   `email` (VARCHAR, Único): Dirección de correo electrónico única.

#### **Tabla `posts`**
Contiene todas las publicaciones creadas por los usuarios.
-   `id` (BIGINT, Clave Primaria): Identificador único para cada publicación.
-   `title` (VARCHAR): Título de la publicación.
-   `content` (TEXT): Contenido principal de la publicación.
-   `created_at` (TIMESTAMP): Fecha y hora de creación.
-   `user_id` (BIGINT, Clave Foránea): Referencia al `id` del usuario que creó la publicación.

#### **Tabla `comments`**
Guarda los comentarios que los usuarios realizan en las publicaciones.
-   `id` (BIGINT, Clave Primaria): Identificador único para cada comentario.
-   `text` (VARCHAR): El contenido del comentario.
-   `created_at` (TIMESTAMP): Fecha y hora de creación del comentario.
-   `user_id` (BIGINT, Clave Foránea): Referencia al `id` del usuario que escribió el comentario.
-   `post_id` (BIGINT, Clave Foránea): Referencia al `id` de la publicación a la que pertenece el comentario.

### Elección de la Base de Datos: PostgreSQL

Para este proyecto, se ha elegido **PostgreSQL** como sistema de gestión de bases de datos. La elección se justifica por las siguientes razones:

1.  **Robustez y Fiabilidad:** PostgreSQL es conocido por su arquitectura robusta y su estricta conformidad con el estándar SQL y los principios ACID, lo que garantiza una alta integridad y fiabilidad de los datos.
2.  **Escalabilidad:** Ofrece un excelente rendimiento en consultas complejas y un manejo eficiente de grandes volúmenes de datos, lo que asegura que la aplicación pueda escalar a futuro sin problemas.
3.  **Tipos de Datos Avanzados:** Proporciona un soporte nativo para una amplia variedad de tipos de datos (como JSONB, Arrays, etc.), lo que brinda flexibilidad para extender las funcionalidades del blog en el futuro si fuera necesario.
4.  **Comunidad y Ecosistema:** Cuenta con una comunidad activa y un ecosistema de herramientas y extensiones muy maduro, lo que facilita el desarrollo, la administración y la resolución de problemas.

Aunque MySQL también es una opción viable, la superioridad de PostgreSQL en cuanto a integridad de datos y características avanzadas lo convierte en la opción ideal para construir una base sólida para esta aplicación.

---

## Instalación y Ejecución

### Prerrequisitos

*   Git
*   Python 3.9+
*   Poetry
*   Docker y Docker Compose

### Opción 1: Ejecución con Docker (Recomendado)

Este método levantará tanto la API como la base de datos en contenedores aislados, gestionando la red y las variables de entorno automáticamente.

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/Hyp3Boy/API-REST-para-un-Mini-Blog.git
    cd API-REST-para-un-Mini-Blog
    ```

2.  **Crear el archivo de entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido. Docker Compose lo usará para configurar los contenedores.
    ```env
    # Variables para la Base de Datos (usadas por los servicios 'db' y 'api')
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    POSTGRES_DB=mini_blog_db
    POSTGRES_HOST=db  # <-- Nombre del servicio de la base de datos en docker-compose.yml

    # URL de conexión para la aplicación (usada por el servicio 'api')
    DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}

    # Entorno de la aplicación
    ENVIRONMENT=development
    ```

3.  **Construir y levantar los contenedores:**
    Este comando construirá la imagen de la API, descargará la de PostgreSQL y pondrá en marcha ambos servicios.
    ```bash
    docker compose up --build
    ```
    La primera vez que se ejecute, el servicio de la API aplicará automáticamente las migraciones de Alembic a la base de datos antes de iniciar el servidor.

4.  **Acceder a la API:**
    *   La API estará disponible en `http://localhost:8000`.
    *   La documentación interactiva (Swagger UI) se encuentra en `http://localhost:8000/docs`.

### Opción 2: Ejecución Local con Poetry

Este método es útil si prefieres ejecutar la aplicación directamente en tu máquina local, pero requiere que tengas una instancia de PostgreSQL corriendo por separado.

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/Hyp3Boy/API-REST-para-un-Mini-Blog.git
    cd API-REST-para-un-Mini-Blog
    ```

2.  **Instalar dependencias:**
    ```bash
    poetry install
    ```

3.  **Configurar el archivo de entorno:**
    Crea un archivo `.env` en la raíz del proyecto. **Nota que `POSTGRES_HOST` ahora es `localhost`**, ya que la base de datos se ejecuta en tu máquina local.
    ```env
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    POSTGRES_DB=mini_blog_db
    POSTGRES_HOST=localhost # <-- ¡Importante!

    DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}
    ENVIRONMENT=development
    ```

4.  **Aplicar las migraciones a la base de datos:**
    ```bash
    poetry run alembic upgrade head
    ```

5.  **Ejecutar el servidor:**
    ```bash
    poetry run uvicorn src.api_rest_mini_blog.main:app --reload
    ```
    La API estará disponible en `http://localhost:8000`.

---

## Ejecución de las Pruebas

Las pruebas están configuradas para ejecutarse contra una base de datos de prueba separada y efímera.

1.  **Configurar la URL de la base de datos de prueba:**
    Asegúrate de tener la variable `TEST_DATABASE_URL` definida en tu archivo `.env`. El framework de pruebas la usará automáticamente.
    ```env
    # .env
    # ... otras variables ...
    TEST_DATABASE_URL=postgresql+asyncpg://testuser:testpassword@localhost:5432/test_mini_blog_db
    ```

2.  **Ejecutar Pytest:**
    Desde la raíz del proyecto, ejecuta el siguiente comando:
    ```bash
    poetry run pytest -v
    ```
    El script de pruebas se encargará de crear y destruir la base de datos de prueba automáticamente.

---

## Ejemplos de Uso con cURL

A continuación se muestran ejemplos para interactuar con los endpoints de la API. (Nota: los IDs pueden variar al ejecutar las pruebas).

### Usuarios

**1. Crear un nuevo usuario**
```bash
curl -X 'POST' \
  'http://localhost:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "testuser",
    "email": "test@example.com"
  }'
```

**2. Obtener detalles de un usuario**
```bash
curl -X 'GET' \
  'http://localhost:8000/users/1' \
  -H 'accept: application/json'
```

### Publicaciones (Posts)

**1. Crear una nueva publicación (suponiendo que el user_id=1 existe)**
```bash
curl -X 'POST' \
  'http://localhost:8000/posts/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Mi primer post",
    "content": "Este es el contenido de mi primer post.",
    "user_id": 1
  }'
```

**2. Obtener las últimas publicaciones**
```bash
curl -X 'GET' \
  'http://localhost:8000/posts/' \
  -H 'accept: application/json'
```

**3. Obtener una publicación específica con sus comentarios**
```bash
curl -X 'GET' \
  'http://localhost:8000/posts/1' \
  -H 'accept: application/json'
```

### Comentarios (Comments)

**1. Añadir un nuevo comentario a una publicación (suponiendo post_id=1 y user_id=1)**
```bash
curl -X 'POST' \
  'http://localhost:8000/posts/1/comments' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "¡Qué gran publicación!",
    "user_id": 1
  }'
```

---

## Fase 5: Prompt para Asistente de IA

Este meta-prompt está diseñado para instruir a un asistente de IA (como Gemini en VS Code o GitHub Copilot Chat) para que actúe como un experto durante el desarrollo de este proyecto, asegurando que el código generado se alinee con las tecnologías, patrones y buenas prácticas definidas.

```markdown
# Meta-Prompt para Asistente de Desarrollo de API con FastAPI

### **Persona y Tono**

Actúa como un desarrollador backend senior experto en Python y FastAPI. Tu enfoque principal es la calidad del código, la eficiencia, la mantenibilidad y la adhesión a las mejores prácticas de la industria. Escribe código limpio, bien documentado y robusto. Sé proactivo al sugerir mejoras y al señalar posibles problemas.

### **1. Contexto del Proyecto**

Estamos construyendo el backend para un sistema de mini-blog. Tu tarea es ayudar a desarrollar, probar y mejorar el código.

El stack tecnológico es estricto y debes adherirte a él en todo momento:
- **Lenguaje:** Python 3.9+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0 (sintaxis asíncrona con `AsyncSession`)
- **Validación de Datos:** Pydantic
- **Gestión de Dependencias:** Poetry
- **Migraciones de Base de Datos:** Alembic
- **Framework de Pruebas:** Pytest (con `pytest-asyncio`)

### **2. Principios de Código y Buenas Prácticas**

- **Claridad y Legibilidad:** Genera código limpio y fácil de entender. Usa nombres de variables y funciones descriptivos y en inglés (ej: `get_user_by_id` en lugar de `get_usr`).
- **Principios SOLID y DRY:** Tu código debe seguir los principios SOLID. Evita la duplicación de código (Don't Repeat Yourself). Encapsula la lógica de negocio en las capas de servicio.
- **Tipado Estricto:** Utiliza `type hints` de forma exhaustiva para todas las variables, argumentos de funciones y valores de retorno. Usa los tipos del módulo `typing` de Python cuando sea necesario.
- **Comentarios:** Añade comentarios o docstrings concisos y útiles para explicar lógica compleja, pero evita comentar código obvio. El código debe ser auto-explicativo en la medida de lo posible.

### **3. Especificidades de FastAPI y Estructura del Proyecto**

Sigue rigurosamente la estructura y patrones de este proyecto:

- **Separación de Responsabilidades:**
    - `routers/`: Contiene los endpoints de la API. Su única responsabilidad es recibir peticiones HTTP, validar datos básicos y llamar a la capa de servicios.
    - `services/`: Contiene toda la lógica de negocio y las operaciones CRUD. Interactúa con la base de datos a través de los modelos.
    - `schemas/`: Contiene los modelos de Pydantic para la validación de datos de entrada (`Create` schemas) y la serialización de datos de salida (schemas de respuesta).
    - `models/`: Contiene los modelos de SQLAlchemy que definen las tablas de la base de datos.
- **Inyección de Dependencias:** Para obtener una sesión de base de datos (`AsyncSession`), utiliza siempre la inyección de dependencias de FastAPI. **Nunca** crees una sesión manualmente en un endpoint.
    - **Ejemplo Correcto:** `async def my_endpoint(db: AsyncSession = Depends(get_db)):`
- **Operaciones Asíncronas:** Todas las interacciones con la base de datos deben ser asíncronas. Usa `await` para todas las llamadas a la base de datos a través de la capa de servicios.
- **Códigos de Estado HTTP:** Devuelve siempre los códigos de estado HTTP más apropiados. Por ejemplo:
    - `200 OK` para respuestas exitosas a `GET`.
    - `201 Created` para la creación exitosa de un recurso (`POST`).
    - `204 No Content` para eliminaciones exitosas.
    - `400 Bad Request` para errores de validación de Pydantic.
    - `404 Not Found` si un recurso solicitado no existe.
    - `409 Conflict` si se intenta crear un recurso que entra en conflicto con uno existente (ej: email duplicado).

### **4. Pruebas Unitarias**

Cuando se te pida generar pruebas, sigue estas directrices:

- **Framework:** Utiliza siempre `pytest` y `pytest-asyncio`.
- **Cliente de Pruebas:** Usa `httpx.AsyncClient` para realizar peticiones a la aplicación.
- **Fixtures:** Crea fixtures reutilizables (`@pytest_asyncio.fixture`) para generar datos de prueba (ej: un usuario o un post) y para proporcionar el `db_session` y el `client`. Esto es preferible a crear los datos manualmente en cada test.
- **Cobertura de Casos:** Asegúrate de probar tanto los "happy paths" (casos de éxito) como los casos de error y "edge cases". Por ejemplo:
    - ¿Qué pasa si intento obtener un post con un ID que no existe? (Debería devolver 404).
    - ¿Qué pasa si intento crear un usuario con un email que ya está en uso? (Debería devolver 409 o 400).
    - ¿Qué pasa si faltan campos en el JSON de una petición `POST`? (Pydantic debería devolver 422).
```