# Sistema de Clínica Dental 🦷

Sistema integral de gestión para clínicas dentales desarrollado con Django, que permite administrar pacientes, tratamientos, odontogramas y financiamientos de manera eficiente.

## 🚀 Características Principales

### 👥 Gestión de Usuarios
- **Tipos de usuario**: Doctor, Secretaria, Paciente, Asistente
- Sistema de autenticación y permisos
- Información completa: teléfono, fecha de nacimiento, dirección

### 🏥 Gestión de Pacientes
- Registro completo de pacientes
- Listado con búsqueda y filtros
- Operaciones CRUD (Crear, Leer, Actualizar, Eliminar)

### 🔬 Especialidades y Tratamientos
- Catálogo de especialidades médicas
- Gestión de tratamientos con precios
- Asignación de especialistas
- Seguimiento de tratamientos aplicados

### 🦷 Odontograma Digital
- Representación visual de la dentadura
- Clasificación de dientes (permanentes/temporales)
- Carga de imágenes para cada diente
- Interfaz intuitiva para el diagnóstico

### 💰 Sistema de Financiamiento
- **Calculadora inteligente** con IA (Groq API)
- Cálculo automático de cuotas mensuales
- Tabla de amortización detallada
- Múltiples tasas de interés configurables
- Generación de cotizaciones en formato Markdown

### 📊 Dashboard Centralizado
- Acceso rápido a funciones principales
- Interfaz moderna con Bootstrap 5
- Navegación intuitiva

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.5
- **Gestor de paquetes**: uv (Astral) - Gestor ultrarrápido de Python
- **Frontend**: Bootstrap 5, FontAwesome
- **Base de datos**: SQLite (desarrollo)
- **IA**: Groq API para cálculos financieros
- **Formularios**: Crispy Forms + Bootstrap 5
- **Procesamiento**: Markdown2 para documentos
- **Imágenes**: Pillow para manejo de archivos

## ⚙️ Instalación y Configuración

### Prerrequisitos
- Python 3.13 o superior
- uv (gestor de paquetes ultrarrápido de Astral)

### 1. Instalar uv
```bash
# En macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# En Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd clinicadental-software
```

### 3. Instalar Dependencias
```bash
# uv automáticamente crea el entorno virtual y instala las dependencias
uv sync
```

### 4. Activar el Entorno Virtual
```bash
# uv crea automáticamente el entorno, solo necesitas activarlo
source .venv/bin/activate  # En macOS/Linux
# o
.venv\Scripts\activate     # En Windows
```

### 5. Configurar Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:
```env
GROQ_API_KEY=tu_api_key_de_groq
```

### 6. Ejecutar Migraciones
```bash
cd backend
python manage.py migrate
```

### 7. Crear Superusuario
```bash
python manage.py createsuperuser
```

### 8. Ejecutar el Servidor
```bash
python manage.py runserver
```

El sistema estará disponible en: `http://localhost:8000`

## 📁 Estructura del Proyecto

```
backend/
├── core/              # App principal (usuarios, dashboard)
├── patients/          # Gestión de pacientes
├── treatments/        # Tratamientos y especialidades
├── odontogram/        # Odontograma digital
├── financing/         # Sistema de financiamiento
├── templates/         # Plantillas HTML compartidas
└── media/            # Archivos multimedia (imágenes)
```

## 🎯 Módulos Principales

### 1. Core (Núcleo)
- **UserModel**: Usuarios del sistema con tipos específicos
- **AuditModel**: Modelo base con auditoría automática
- **Dashboard**: Página principal con accesos rápidos

### 2. Patients (Pacientes)
- Registro y gestión completa de pacientes
- Formularios con validación
- Sistema de permisos por rol

### 3. Treatments (Tratamientos)
- **SpecialtyModel**: Especialidades médicas
- **TreatmentsModel**: Catálogo de tratamientos
- **AppliedTreatmentsModel**: Tratamientos aplicados a pacientes
- Wizard multistep para aplicar tratamientos

### 4. Odontogram (Odontograma)
- **TeethModel**: Modelo de dientes con imágenes
- Visualización en formato de dentadura completa
- Soporte para dientes permanentes y temporales

### 5. Financing (Financiamiento)
- **InteresRateModel**: Tasas de interés configurables
- Calculadora inteligente con IA
- Generación automática de tablas de amortización
- Cotizaciones profesionales en HTML

## 🤖 Integración con IA

El sistema utiliza la **API de Groq** para generar cálculos financieros precisos:

- Cálculo automático de cuotas mensuales
- Fórmulas de amortización francesa
- Generación de tablas detalladas
- Formateo profesional en Markdown/HTML

## 🔐 Sistema de Permisos

- **LoginRequiredMixin**: Autenticación obligatoria
- **PermissionRequiredMixin**: Permisos específicos por modelo
- Control granular de acceso por tipo de usuario

## 🎨 Interfaz de Usuario

- **Bootstrap 5**: Framework CSS moderno
- **FontAwesome**: Iconografía profesional
- **Crispy Forms**: Formularios estilizados
- **Responsive Design**: Adaptable a dispositivos móviles

## 📋 Estados de Tratamientos

- **CD**: Presupuestado
- **PE**: Pendiente
- **AP**: Aplicado
- **CA**: Cancelado

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades, crear un issue en el repositorio del proyecto.

## 📄 Licencia

Este proyecto está bajo una licencia específica. Consultar el archivo LICENSE para más detalles.

---

## ScreenShots del Sistema


**Desarrollado para la gestión eficiente de clínicas dentales 🦷✨**