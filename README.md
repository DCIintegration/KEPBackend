# Backend KEP (KPIs Eficiencia y Productividad) 🚀

![Django](https://img.shields.io/badge/Django-5.1.7-green)
![DRF](https://img.shields.io/badge/DRF-latest-blue)
![Python](https://img.shields.io/badge/Python-3.x-blue)

## Descripción General 📋

KEP (KPIs Eficiencia y Productividad) es un sistema backend integral diseñado para rastrear, analizar y gestionar indicadores clave de rendimiento para la eficiencia y productividad empresarial. Construido con Django y Django REST Framework, esta aplicación proporciona APIs robustas para la gestión de KPIs, administración de empleados, seguimiento de proyectos y análisis de dashboards.

## Características ✨

- **Sistema de Autenticación Personalizado** - Gestión de usuarios basada en roles con permisos granulares
- **Gestión de KPIs** - Crear, rastrear y analizar diversos indicadores de rendimiento empresarial
- **Seguimiento de Proyectos** - Monitorear proyectos, asignar empleados y controlar horas facturables
- **Panel Administrativo** - Visualizar datos departamentales e información de empleados
- **Procesamiento de Excel/CSV** - Procesadores de archivos integrados para importar y analizar datos empresariales
- **Endpoints API REST** - API bien documentada para integración con frontend

## Arquitectura 🏗️

KEP sigue una arquitectura modular con cuatro aplicaciones Django principales:

1. **custom_auth** - Maneja la autenticación y gestión de usuarios con permisos basados en roles
2. **administracion** - Gestiona funciones administrativas, departamentos y detalles de empleados
3. **dashboard** - Procesa y muestra datos de KPIs y análisis
4. **proyectos** - Administra información de proyectos, asignaciones y asignación de recursos

## Stack Tecnológico 💻

- **Framework**: Django 5.1+
- **API**: Django REST Framework
- **Base de Datos**: SQLite (configurable para bases de datos en producción)
- **Procesamiento de Archivos**: Pandas, OpenPyXL
- **Visualización de Datos**: Soporte para varios formatos a través de serializadores

## Instalación 🛠️

### Requisitos Previos

- Python 3.x
- pip (gestor de paquetes de Python)
- Herramienta de entorno virtual (recomendado)

### Configuración Paso a Paso

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tunombredeusuario/KEP-backend.git
   cd KEP-backend
   ```

2. **Crear y activar un entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

7. **Acceder a la aplicación**
   - Interfaz de administración: http://127.0.0.1:8000/admin/
   - Endpoints de API: http://127.0.0.1:8000/api/

## Endpoints de API 🌐

### Autenticación
- `POST /custom_auth/login/` - Inicio de sesión de usuario
- `GET /custom_auth/view_users/` - Listar todos los usuarios (solo superusuario)
- `POST /custom_auth/create_user/` - Crear nuevo usuario (solo superusuario)
- `PUT /custom_auth/update_user/<id>/` - Actualizar usuario (solo superusuario)
- `DELETE /custom_auth/delete_user/<id>/` - Eliminar usuario (solo superusuario)

### Administración
- `GET /administracion/dashboard_administrativo/` - Vista general del panel administrativo
- `GET /administracion/departamento_detalles/<id>/` - Detalles del departamento
- `GET /administracion/empleado_detalles/<id>/` - Detalles del empleado
- `PUT /administracion/modificar_datos/<id>/` - Modificar datos del empleado

### Dashboard
- `GET /dashboard/main_dashboard/` - Vista general del dashboard de KPIs
- `POST /dashboard/create_KPI/` - Crear nuevo KPI (solo superusuario)
- `PUT /dashboard/update_kpi/<id>/` - Actualizar KPI (solo superusuario/admin)
- `DELETE /dashboard/delete_kpi/<id>/` - Eliminar KPI (solo superusuario)
- `GET /dashboard/kpi_details/<id>/` - Ver detalles del KPI

### Proyectos
- `GET /proyectos/view_logs/` - Ver todos los registros de entrada de KPI
- `GET /proyectos/view_log_details/<id>/` - Ver detalles de un registro específico
- `POST /proyectos/report_log/` - Reportar problemas con datos de registro
- `POST /proyectos/upload_excel_log/` - Subir datos Excel para cálculo de KPI
- `POST /proyectos/upload_manual_log/` - Ingresar datos de KPI manualmente
- `PUT /proyectos/modify_log/<id>/` - Modificar datos de registro existentes (solo superusuario)

## Modelos de Datos 📊

### Gestión de Usuarios

```
Empleado (Usuario Extendido)
├── nombre - Nombre del empleado
├── role - Rol del usuario (ingenieria, administracion, gerencia, superusuario)
├── puesto - Posición laboral
├── fecha_contratacion - Fecha de contratación
├── activo - Estado activo
├── sueldo - Salario
├── departamento - Departamento (Clave Foránea)
├── email - Correo electrónico (único)
├── facturable - Estado facturable
```

### Sistema de KPI

```
KpiInputData
├── total_horas_facturables - Total de horas facturables
├── total_horas_planta - Total de horas en planta
├── total_horas_facturadas - Total de horas facturadas
├── numero_empleados - Número de empleados
├── numero_empleados_facturables - Número de empleados facturables
├── dias_trabajados - Días trabajados
├── costo_por_hora - Costo por hora
├── ganancia_total - Ganancia total
├── status - Estado (correcto, reportado, corregido)

Kpi
├── code - Código KPI (ELDR, RE, RBE, UBH, etc.)
├── name - Nombre del KPI
├── description - Descripción
├── data - Datos de entrada (Clave Foránea)
├── value - Valor calculado
```

### Gestión de Proyectos

```
Proyecto
├── nombre - Nombre del proyecto
├── descripcion - Descripción
├── fecha_inicio - Fecha de inicio
├── fecha_fin_estimada - Fecha estimada de finalización
├── fecha_fin_real - Fecha real de finalización
├── estado - Estado (planificacion, desarrollo, testing, etc.)
├── presupuesto - Presupuesto
├── empleados - Empleados (Muchos a muchos a través de AsignacionProyecto)

AsignacionProyecto
├── proyecto - Proyecto (Clave Foránea)
├── empleado - Empleado (Clave Foránea)
├── rol - Rol en el proyecto
├── fecha_inicio - Fecha de inicio
├── fecha_fin - Fecha de finalización
├── horas_asignadas - Horas asignadas
├── horas_reales - Horas reales
├── es_facturable - Estado facturable
├── costo_hora - Costo por hora
├── tarifa_hora - Tarifa por hora
```

## Consideraciones de Seguridad 🔒

- El sistema utiliza el sistema de autenticación integrado de Django, extendido con modelos de usuario personalizados
- El control de acceso basado en roles está implementado en toda la aplicación
- La autenticación basada en JWT o sesiones puede configurarse según los requisitos
- Todos los endpoints sensibles requieren autenticación
- **Importante:** La clave secreta de Django en settings.py debe cambiarse y almacenarse de forma segura para producción

## Directrices de Desarrollo 📝

1. **Estilo de Código**: Seguir PEP 8 y los estándares de codificación de Django
2. **Documentación**: Documentar todas las funciones, clases y endpoints
3. **Pruebas**: Escribir pruebas para nuevas características y asegurarse de que pasen antes de enviar
4. **Ramificación**: Usar ramas de características y enviar solicitudes de extracción para revisión
5. **Seguridad**: Nunca confirmar credenciales sensibles en el repositorio

## Despliegue 🌩️

Para despliegue en producción:

1. Establecer `DEBUG = False` en settings.py
2. Configurar una base de datos lista para producción (se recomienda PostgreSQL)
3. Configurar el servicio adecuado de archivos estáticos
4. Usar un servidor WSGI como Gunicorn
5. Configurar un proxy inverso (Nginx/Apache)
6. Configurar HTTPS
7. Usar variables de entorno para configuraciones sensibles

## Contribuir 🤝

1. Hacer un fork del repositorio
2. Crear una rama de características (`git checkout -b feature/caracteristica-asombrosa`)
3. Confirmar tus cambios (`git commit -m 'Añadir característica asombrosa'`)
4. Empujar a la rama (`git push origin feature/caracteristica-asombrosa`)
5. Abrir una Solicitud de Extracción

## Licencia 📄

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.

## Agradecimientos 🙏

- A la comunidad de Django por el increíble framework
- A todos los contribuyentes que han ayudado a dar forma a este proyecto
- Un agradecimiento especial al equipo de Integración DEI por su continuo apoyo

---

© 2025 Equipo de Desarrollo KEP. Todos los derechos reservados.
