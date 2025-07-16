# 💅 Sistema de Turnos - Centro de Estética

Aplicación de escritorio desarrollada en Python para la gestión integral de turnos, clientes, empleados y planes en centros de estética. Pensada para facilitar el trabajo en la recepción del local, esta herramienta permite registrar sesiones, organizar horarios, calcular pagos semanales del personal y administrar los planes contratados por las clientas.

---

## 🖥️ Características principales

- 📅 **Turnos semanales**: Vista de calendario de lunes a sábado de 7 a 20 hs.
- 👥 **Gestión de clientas**:
  - Registro y edición de datos.
  - Seguimiento de número de sesiones utilizadas.
  - Estado de pago de cada plan.
- 🧑‍🔧 **Gestión de empleados**:
  - Registro de ingresos y egresos con cálculo automático de horas trabajadas.
  - Pago por hora configurado individualmente.
  - Cálculo acumulado del total a cobrar cada viernes.
- 💳 **Planes de tratamiento**:
  - Registro y asignación de planes personalizados a cada clienta.
  - Control de sesiones restantes.
- 💬 **Preparado para integración futura con WhatsApp** para envío de recordatorios.
- 🎨 Interfaz personalizada con imagen de fondo y navegación amigable.

---

## 🛠️ Tecnologías utilizadas

- **Lenguaje**: Python 3.12
- **Interfaz gráfica**: Tkinter
- **Base de datos**: MySQL
- **Paradigma**: Arquitectura modular (MVC)
- **Herramientas complementarias**:
  - `ttk` para widgets estilizados.
  - `datetime` para manejo de fechas y horarios.
  - `tkcalendar` (si se utiliza calendario visual).

---

## 🚀 Cómo ejecutar el proyecto

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/turnero-estetica.git
cd turnero-estetica


