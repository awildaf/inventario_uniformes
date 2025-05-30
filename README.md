# Sistema de Inventario de Uniformes para Hoteles

## Estructura del Proyecto

- `models.py`: Modelos de base de datos con SQLAlchemy.
- `database.py`: Inicialización de la base de datos y conexión.
- `sample_data.py`: Inserción de datos de prueba.
- `main.py`: Ventana principal de la aplicación (PyQt5).
- `requirements.txt`: Dependencias del proyecto.
- `ui/`: Formularios CRUD de Uniformes, Empleados y Asignaciones.

## Cómo comenzar

1. Clona el repositorio:
    ```
    git clone https://github.com/awildaf/inventario_uniformes.git
    cd inventario_uniformes
    ```

2. Instala las dependencias:
    ```
    pip install -r requirements.txt
    ```

3. Ejecuta la aplicación (esto inicializa la base de datos y carga los datos de prueba):
    ```
    python main.py
    ```

4. Usa el menú "Gestión" para acceder a Uniformes, Empleados y Asignaciones.

## Próximos pasos

- Implementar generación de recibos y facturas en PDF.
- Añadir reportes e informes estadísticos.
- Mejorar la experiencia visual de la interfaz.