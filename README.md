# API REST para un Mini-Blog

Este proyecto es el backend para un sistema de mini-blog que permite a los usuarios registrarse, crear publicaciones y comentar en las publicaciones de otros.

## Fase 1: Diseño y Modelado de la Base de Datos

### Diagrama Entidad-Relación (E/R)

A continuación se muestra el diagrama E/R que representa la estructura de la base de datos del proyecto.

![Diagrama E/R](docs/diagrama.jpg)

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