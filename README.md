## Install Dependencies
```bash 
pip3 install -r requirements.txt
```

# FastAPI + Google Sheets Integration 🚀

Guía técnica para conectar una API desarrollada en FastAPI con Google Sheets utilizando una Cuenta de Servicio (Service Account).

## 🎯 Objetivo
El propósito de este módulo es permitir que el backend realice las siguientes acciones sin intervención manual:
* **Leer datos** de una hoja de cálculo.
* **Agregar filas** dinámicamente.
* Mantener la independencia entre el entorno (local/prod) y la lógica de negocio.

## 🧱 Conceptos Clave
* **Usuario Técnico:** El backend no utiliza tus credenciales personales; se autentica mediante una Service Account.
* **Permisos:** El Google Sheet debe compartirse explícitamente con el email de la Service Account.
* **Abstracción:** Pensalo como un usuario técnico con permisos sobre una tabla específica.

---

## 🛠️ Configuración Paso a Paso

### 1. Preparación en Google Cloud
1. **Proyecto:** Crea un nuevo proyecto en [Google Cloud Console](https://console.cloud.google.com/).
2. **Habilitar API:** Activa la **Google Sheets API** desde la Library.
3. **Credenciales:** Crea una **Service Account** (ej: `fastapi-sheets-sa`).
4. **JSON Key:** Genera y descarga una llave en formato JSON. 
    * ⚠️ **Seguridad:** No subas este archivo a Git; agrégalo a tu `.gitignore`.

### 2. Vinculación con el Sheet
1. **Compartir:** Abre tu Google Sheet, haz clic en **Share** y agrega el email de la Service Account con permiso de **Editor**. *Sin esto recibirás un error 403 Forbidden*.
2. **ID del Sheet:** Copia el ID desde la URL del navegador (el código entre `/d/` y `/edit`).

---

## 📂 Estructura del Proyecto
```text
project-root/
  service-account.json  <-- Archivo de credenciales
  domain/               <-- Lógica pura
  infrastructure/       <-- Cliente de Google Sheets
  adapters/             <-- Adaptadores de datos
```

 ##  🔌 Implementación Técnica
Cliente de Infraestructura
Este componente inicializa la conexión utilizando los alcances (scopes) necesarios.

```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "service-account.json"


def get_sheets_service():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)
```


### Operaciones de Datos

Lectura: Obtiene los valores de un rango definido (ej: Usuarios!A2:D) y los mapea a objetos ExcelData.


Escritura: Utiliza el método append con valueInputOption="USER_ENTERED" para insertar nuevas filas al final de la tabla.

## 🧠 Buenas Prácticas

Desacoplamiento: El dominio no sabe que los datos vienen de Sheets.


Flexibilidad: Cambiar de base de datos o de cuenta es tan simple como cambiar el ID o el archivo JSON, sin tocar el código de negocio.


Perspectiva: El Sheet se trata como un repositorio transaccional ligero.

🏁 Estado: Lectura, escritura y arquitectura limpia funcionando correctamente.

## 🔁 Para conectar una NUEVA cuenta / Sheet

Crear nuevo proyecto o nueva Service Account

Descargar nuevo .json

Compartir el Sheet con esa SA

Cambiar:

service-account.json

SPREADSHEET_ID

👉 No se toca código de negocio