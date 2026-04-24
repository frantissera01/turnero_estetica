# 💼 Sistema de Turnos - Centro de Estética

Aplicación de escritorio desarrollada en **Python + Tkinter + MySQL** para gestionar turnos, clientas, empleados, horarios trabajados, pagos y planes de tratamiento en un centro de estética real.

> Proyecto en desarrollo, creado a partir de una necesidad real de negocio.

---

## 🚀 Funcionalidades principales

- 📅 Gestión de turnos de lunes a sábado, de 7 a 20 hs.
- 👥 Gestión de clientas con datos de contacto, sesiones y estado de pago.
- 💳 Registro y asignación de planes de tratamiento.
- 👨‍💼 Gestión de empleados.
- ⏱️ Registro de ingreso y egreso de empleados.
- 💰 Cálculo de horas trabajadas y pagos.
- 🧠 Lógica de negocio orientada a uso real en recepción.

---

## 🧠 Lógica de negocio

- Control de turnos por fecha y horario.
- Relación entre turnos y clientas mediante `cliente_id`.
- Seguimiento de sesiones usadas/restantes por plan.
- Registro de horarios de empleados.
- Cálculo de saldos pendientes para pagos a empleados.

---

## 🛠️ Tecnologías

- Python 3.12
- Tkinter
- MySQL
- mysql-connector-python
- Pillow
- tkcalendar
- Arquitectura modular basada en MVC

---

## 📁 Estructura del proyecto

```text
turnero_estetica/
├── assets/              # Recursos gráficos
├── config/              # Configuración de base de datos
├── controllers/         # Controladores
├── database/            # Script SQL de base de datos
├── models/              # Modelos y consultas SQL
├── tests/               # Tests básicos
├── ui/                  # Tema visual
├── utils/               # Funciones auxiliares
├── views/               # Pantallas Tkinter
├── main.py              # Punto de entrada
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/frantissera01/turnero_estetica.git
cd turnero_estetica
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

Activar entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo de ejemplo:

```bash
copy .env.example .env
```

Editar `.env` con tus datos locales de MySQL:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=turnero_estetica
DB_PORT=3306
```

### 5. Crear la base de datos

Ejecutar el script:

```bash
mysql -u root -p < database/schema.sql
```

O importarlo manualmente desde MySQL Workbench / phpMyAdmin.

### 6. Ejecutar la aplicación

```bash
python main.py
```

---

## 🧪 Tests

Ejecutar tests:

```bash
pytest
```

---

## 📸 Screenshots

Próximamente: capturas de pantalla de la gestión de turnos, clientas, empleados y planes.

---

## 🚧 Estado del proyecto

En desarrollo. El objetivo es convertirlo en una herramienta de escritorio estable para uso interno en recepción, con mejoras progresivas en validaciones, reportes y automatización.

---

## 📌 Autor

Desarrollado por **Franco Tissera** como proyecto real de gestión para un centro de estética.
