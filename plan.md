Alcance del Sistema:
Migración de persistencia plana (JSON) a base de datos relacional (SQLite). Implementación de operaciones CRUD completas con validación de tipos de datos y borrado lógico para auditoría. Integración de Autenticación nativa de Django y Autorización basada en roles (RBAC) mediante grupos y decoradores a nivel de servidor.

MoSCoW Actualizado:
• Must: SQLite, CRUD completo, Login y Roles (Admin, Normal, Viewer), Borrado lógico, Variables de entorno (.env).
• Should: Carga masiva mediante CSV.
• Could: Alertas automatizadas por correo.
• Won't: API REST externa.