# 📊 Gestión de precios - Sistema Web de Gestión

Una **aplicación web completa** para la gestión centralizada de proveedores, artículos, descuentos y cotizaciones de dólar integrada con **SQL Server**.

## 🎯 Características Principales

### ✅ Módulo Proveedores
- Crear nuevos proveedores
- Editar información de proveedores
- Eliminar proveedores (con validación referencial)
- Listado completo de proveedores

### ✅ Módulo Artículos
- Carga de productos con múltiples atributos (Marca, Categoría, SKU, Costo, IVA)
- **Buscador en tiempo real** por SKU, ID o nombre de producto
- **Paginación inteligente** (50 artículos por página)
- Conversión automática de IVA (1 = 21%, 2 = 10.5%)
- Integración con proveedores

### ✅ Módulo Descuentos
- Gestión avanzada de descuentos por proveedor
- 4 tipos de descuentos: Descuento 1, Descuento 2, Pago Contado, Descuento Financiero
- **Creación de nuevos descuentos** con prevención de duplicados
- Dropdown inteligente que deshabilita proveedores ya registrados
- Insert/Update automático

### ✅ Módulo Dólar
- **Dólar Proveedores**: Cotización específica para cada proveedor
- **Dólar Oficial**: Histórico de cotizaciones oficiales con paginación (50 registros/página)
- Edición y eliminación de registros
- Interfaz con 2 tabs para fácil navegación

---

## 🛠️ Tecnología Utilizada

| Componente | Versión |
|-----------|---------|
| **Python** | 3.13.3+ |
| **Flask** | 2.x+ |
| **SQL Server** | 2016+ |
| **pyodbc** | 4.x+ |
| **HTML/CSS/JavaScript** | ES6+ |

### Dependencias Python
```
Flask==2.3.0
pyodbc==4.0.35
python-dotenv==1.0.0
```

---

## 📋 Requisitos Previos

- **Python 3.13+** instalado
- **SQL Server 2016+** accesible
- **ODBC Driver 17 for SQL Server** instalado
- Base de datos **Prueba2** con las tablas necesarias
- Acceso a Windows Authentication o SQL Server Authentication

---

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/gestion-prueba2.git
cd gestion-prueba2
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# Configuración de SQL Server - Windows Authentication
SQL_SERVER=DESKTOP-CGECVO9\SQLEXPRESS
SQL_DATABASE=Prueba2
SQL_DRIVER=ODBC Driver 17 for SQL Server
FLASK_ENV=development
```

**Para SQL Server Authentication:**
```env
SQL_SERVER=localhost
SQL_DATABASE=Prueba2
SQL_USER=sa
SQL_PASSWORD=tu_contraseña
FLASK_ENV=development
```

### 6. Crear estructura de tablas en SQL Server

Ejecuta el siguiente script en SQL Server Management Studio:

```sql
-- Tabla Proveedores
CREATE TABLE dbo.proveedores (
    id_proveedor INT PRIMARY KEY IDENTITY(1,1),
    nombre_proveedor VARCHAR(255) NOT NULL UNIQUE
);

-- Tabla Artículos
CREATE TABLE dbo.articulos (
    id_articulo INT PRIMARY KEY IDENTITY(1,1),
    id_proveedor INT NOT NULL,
    marca VARCHAR(100),
    categoria VARCHAR(100),
    producto VARCHAR(255) NOT NULL,
    sku VARCHAR(100) NOT NULL UNIQUE,
    iva INT,
    costo_c_iva DECIMAL(18,6),
    tipo_moneda VARCHAR(10),
    fecha_ultima_modificacion DATETIME,
    FOREIGN KEY (id_proveedor) REFERENCES dbo.proveedores(id_proveedor)
);

-- Tabla Descuentos por Proveedor
CREATE TABLE dbo.descuentos_proveedor (
    id_proveedor INT PRIMARY KEY,
    descuento_1 DECIMAL(18,6),
    descuento_2 DECIMAL(18,6),
    pago_contado DECIMAL(18,6),
    dto_financiero DECIMAL(18,6),
    fecha_modificacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_proveedor) REFERENCES dbo.proveedores(id_proveedor)
);

-- Tabla Dólar por Proveedor
CREATE TABLE dbo.dolar_proveedor (
    id_proveedor INT PRIMARY KEY,
    dolar_proveedor DECIMAL(18,6) NOT NULL,
    fecha DATE,
    ultima_actualizacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_proveedor) REFERENCES dbo.proveedores(id_proveedor)
);

-- Tabla Dólar Oficial (Histórico)
CREATE TABLE dbo.hist_Dolar_Oficial (
    id INT PRIMARY KEY IDENTITY(1,1),
    tipo_cambio DECIMAL(18,6) NOT NULL,
    fecha DATE NOT NULL UNIQUE
);
```

### 7. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

---

## 📁 Estructura de Carpetas

```
gestion-prueba2/
│
├── app.py                    # Aplicación principal con rutas Flask
├── database.py               # Módulo de conexión a SQL Server
├── .env                      # Variables de entorno (no subir a Git)
├── .gitignore               # Archivos a ignorar en Git
├── requirements.txt         # Dependencias Python
├── README.md               # Este archivo
│
├── templates/              # Archivos HTML (Jinja2)
│   ├── base.html          # Plantilla base (navbar, estilos CSS)
│   ├── index.html         # Dashboard principal
│   ├── proveedores.html   # Gestión de proveedores
│   ├── articulos.html     # Gestión de artículos
│   ├── descuentos.html    # Gestión de descuentos
│   ├── dolar.html         # Gestión de dólar
│   ├── 404.html           # Página de error 404
│   └── 500.html           # Página de error 500
│
├── venv/                   # Entorno virtual (no subir a Git)
│
└── docs/                   # Documentación adicional
    └── API_ENDPOINTS.md   # Documentación de endpoints
```

---

## 🌐 Rutas Disponibles

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Dashboard principal |
| `/proveedores` | GET | Lista de proveedores |
| `/articulos` | GET | Lista de artículos |
| `/descuentos` | GET | Gestión de descuentos |
| `/dolar` | GET | Gestión de dólar |
| `/api/proveedores/crear` | POST | Crear proveedor |
| `/api/proveedores/<id>/actualizar` | PUT | Actualizar proveedor |
| `/api/proveedores/<id>/eliminar` | DELETE | Eliminar proveedor |
| `/api/articulos/crear` | POST | Crear artículo |
| `/api/descuentos/actualizar/<id>` | PUT | Actualizar/crear descuentos |
| `/api/dolar/cargar/<id>` | POST | Cargar dólar proveedor |
| `/api/dolar/oficial/cargar` | POST | Cargar dólar oficial |
| `/api/dolar/oficial/<fecha>/eliminar` | DELETE | Eliminar dólar oficial |

---

## 💻 Uso de la Aplicación

### Crear un Proveedor
1. Ir a **Proveedores**
2. Click en **➕ Nuevo Proveedor**
3. Ingresar nombre
4. Click **Guardar**

### Cargar Artículos
1. Ir a **Artículos**
2. Click en **➕ Nuevo Artículo**
3. Completar formulario
4. Click **Guardar**

### Buscar Artículos
1. Usar el **buscador** en la sección de Artículos
2. Buscar por: SKU, ID o Nombre de producto
3. La búsqueda es en **tiempo real**

### Gestionar Descuentos
1. Ir a **Descuentos**
2. Para nuevos: Click **➕ Nuevo Descuento**
3. Seleccionar proveedor (solo disponibles sin descuentos)
4. Ingresar descuentos
5. Click **Guardar**

### Cargar Dólar
1. Ir a **Dólar**
2. Seleccionar tab deseado:
   - **Dólar Proveedores**: Carga específica por proveedor
   - **Dólar Oficial**: Histórico de cotizaciones
3. Click **➕ Cargar**
4. Completar datos y guardar

---

## 🔍 Debugging

### Ver conexión a BD
```bash
python test_connection.py
```

### Problemas comunes

**Error: "Cannot insert explicit value for identity column"**
- ✅ Arreglado: El código ahora usa AUTO-INCREMENT automático

**Error: "TemplateNotFound"**
- ✅ Arreglado: Templates 404.html y 500.html incluidos

**Error: "Failed to load resource 500"**
- Revisar consola Flask para detalles del error
- Verificar conexión a SQL Server
- Verificar archivo .env

---

## 📊 Características Avanzadas

### Paginación
- Artículos: **50 por página**
- Dólar Oficial: **50 por página**
- Navegación intuitiva con números de página

### Búsqueda en Tiempo Real
- Busca mientras escribes en Artículos
- Busca por SKU, ID o nombre de producto

### Prevención de Duplicados
- Los proveedores con descuentos se deshabilitan en gris
- No permite crear descuentos duplicados

### Conversión de IVA
- Muestra automáticamente: 1 = 21%, 2 = 10.5%

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 📧 Contacto
https://github.com/blenddzy

---

## 🚀 Roadmap Futuro

- [ ] Autenticación de usuarios
- [ ] Exportar a Excel/PDF
- [ ] Gráficos de análisis
- [ ] Auditoría de cambios
- [ ] Notificaciones por email
- [ ] API REST completa
- [ ] Respaldos automáticos
- [ ] Integración con otras aplicaciones
- [ ] Modo oscuro

---

## 📚 Recursos Útiles

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python pyodbc](https://github.com/mkleehammer/pyodbc)
- [SQL Server Documentation](https://docs.microsoft.com/sql/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

**Hecho con ❤️ por Fede!**

Last Updated: **17/11/2025**
