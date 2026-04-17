# 📂 Mini Proyecto: Google Drive Loader de LangChain

Este proyecto nos servirá para entender cómo conectar nuestra IA con fuentes externas protegidas por permisos, en este caso, **Google Drive**.

> [!WARNING]
> La parte más compleja de este proyecto no es el código de Python, sino la configuración en **Google Cloud Console**. Sigue los pasos de esta guía al detalle.

---

### Paso 1: Configurar Proyecto en Google Cloud Console
1.  **Crea un proyecto:** Accede a [Google Cloud Console](https://console.cloud.google.com/) y crea uno nuevo (ej: "Curso LangChain").
2.  **Habilita la API:** En el buscador superior escribe **"Google Drive API"** y actívala para este proyecto.
3.  **Pantalla de Consentimiento (OAuth):**
    *   Usa el modo "Externo".
    *   Nombre de la App: "App LangChain Udemy".
    *   Email de soporte: El tuyo.
    *   **IMPORTANTE:** En "Test Users", añade tu propio correo de Gmail. Sin esto, Google bloqueará el acceso mientras la app esté en modo pruebas.
4.  **Crea Credenciales:**
    *   Menú lateral -> Credenciales -> Crear Credenciales -> **ID de Cliente OAuth**.
    *   Tipo de aplicación: **Aplicación de Escritorio**.
    *   Descarga el archivo JSON resultante y renómbralo como `credentials.json`. 

---

### Paso 2: Preparar tu Google Drive
1.  Crea una carpeta en tu Drive y sube algunos documentos (PDF, Word o TXT).
2.  Obtén el **Folder ID**: Entra en esa carpeta desde el navegador y copia el código que aparece al final de la URL (ej: `1A2B3C...`).

---

### Paso 3: Funcionamiento del Loader
Cuando ejecutes el programa:
1.  Se abrirá tu navegador para pedirte permiso.
2.  Al aceptar, se generará localmente un archivo `token.json`. 
3.  Ese token permitirá que el programa acceda a Drive en el futuro automáticamente, sin volver a pedir permisos en el navegador.

---

### Librerías Necesarias
Para este proyecto hemos instalado las siguientes bibliotecas de integración oficial de Google:
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib langchain-google-community
```
