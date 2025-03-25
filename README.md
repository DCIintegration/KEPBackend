# KEP (KPIs Eficiencia y Productividad) Backend 🚀

Este proyecto es el backend del sistema KEP, desarrollado en Python utilizando el framework Django. Proporciona la lógica de negocio y la gestión de datos para la plataforma KEP. 💻🔧

## Tabla de Contenidos 📑
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura de la Base de Datos](#estructura-de-la-base-de-datos)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Estructura del Proyecto 📁

El proyecto se organiza en varios módulos clave para mantener todo estructurado y organizado:

- **KEP/**: Contiene la configuración principal de Django 🛠️.
- **administracion/**: Módulo encargado de la administración de usuarios y permisos 👥.
- **custom_auth/**: Maneja la autenticación personalizada de usuarios 🔑.
- **dashboard/**: Gestiona la lógica del panel de control 📊.
- **kpi_output/**: Responsable de la generación y gestión de indicadores clave de rendimiento (KPIs) 📈.
- **proyectos/**: Administra la creación y seguimiento de proyectos 📅.

## Requisitos Previos 🧑‍💻

Antes de empezar, asegúrate de tener instalados los siguientes componentes:

- **Python 3.x** 🐍
- **Django** 🖥️
- **SQLite** (o el gestor de base de datos que prefieras) 🗄️

## Instalación 🛠️

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/DCIintegration/KEP_backend.git

2. **Navegar al directorio del proyecto**:
   ```bash
   cd KEP_backend
   ```

3. **Crear y activar un entorno virtual**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # En Windows usa `env\\Scripts\\activate`
   ```

4. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Aplicar migraciones a la base de datos**:
   ```bash
   python manage.py migrate
   ```

6. **Crear un superusuario**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Iniciar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

   Accede a `http://localhost:8000/` en tu navegador. 🌐

## Uso 🔍

- **Panel de Administración**: Accede a `http://localhost:8000/admin/` e inicia sesión con el superusuario creado anteriormente para gestionar los modelos y datos de la aplicación. 👨‍💻
  
- **APIs**: Revisa los archivos `urls.py` en cada módulo para conocer las rutas disponibles. 🚀

## Estructura de la Base de Datos 🗃️

La base de datos sigue un esquema relacional con los siguientes modelos principales:

### Modelo `Usuario` 👤
Este modelo gestiona la información de los usuarios del sistema, como roles y autenticación.

```python
class Usuario(AbstractUser):
    rol = models.CharField(max_length=50, choices=[('Ingeniería', 'Ingeniería'), ('Administración', 'Administración'), ('Gerencia', 'Gerencia'), ('Superusuario', 'Superusuario')])
```

- **rol**: Define el rol del usuario en el sistema (Ingeniería, Administración, Gerencia, Superusuario). Solo el Superusuario puede crear otros usuarios.

### Modelo `Proyecto` 📂
Este modelo administra la información sobre los proyectos en el sistema.

```python
class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE)
```

- **nombre**: Nombre del proyecto.
- **descripcion**: Descripción detallada del proyecto.
- **fecha_inicio**: Fecha de inicio del proyecto.
- **fecha_fin**: Fecha de finalización del proyecto (opcional).
- **responsable**: El usuario encargado del proyecto (relación con el modelo `Usuario`).

### Modelo `KPI` 📊
Este modelo se encarga de gestionar los indicadores clave de rendimiento (KPIs) de cada proyecto.

```python
class KPI(models.Model):
    nombre = models.CharField(max_length=255)
    valor = models.FloatField()
    fecha = models.DateField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
```

- **nombre**: Nombre del KPI (por ejemplo, "Ventas trimestrales").
- **valor**: El valor asociado al KPI (por ejemplo, "5000").
- **fecha**: Fecha en la que se registró el KPI.
- **proyecto**: El proyecto asociado a este KPI (relación con el modelo `Proyecto`).

## Contribuciones 🤝

Si deseas contribuir a este proyecto, sigue estos pasos:

1. **Realiza un fork del repositorio**: Haz clic en el botón "Fork" en GitHub.
2. **Crea una nueva rama con tu cambio**: Usa un nombre descriptivo para la rama.
3. **Haz commit de tus modificaciones**: Realiza commits claros y descriptivos.
4. **Envía un pull request**: Asegúrate de que tus cambios no rompen nada antes de enviar el pull request.

## Licencia 📜

Este proyecto se distribuye bajo la licencia [MIT](LICENSE). Si deseas más detalles sobre la licencia, revisa el archivo LICENSE del repositorio.

---

¡Gracias por tu interés en contribuir al proyecto! 🙌
```

Este archivo ahora incluye una versión más detallada con emojis para hacerlo más accesible y visualmente atractivo. También he agregado explicaciones más claras de los modelos de base de datos y los roles. ¡Avísame si necesitas más ajustes!
