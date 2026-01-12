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
🧱 FASE 0 — Precondiciones

Vas a necesitar:

✅ Un mail de Google nuevo (ya lo tenés)

✅ Acceso a Google Drive

✅ Acceso a Google Cloud Console

👉 Todo lo que creemos va a pertenecer a ese mail.

☁️ FASE 1 — Crear el proyecto en Google Cloud

Entrá a:
👉 https://console.cloud.google.com

Arriba a la izquierda → Select project

New Project

Nombre: fastapi-sheets (o el que quieras)

Organization: none

Location: default

Create

📌 Asegurate de que el proyecto quede seleccionado arriba.

📦 FASE 2 — Habilitar la API de Google Sheets

Menú lateral → APIs & Services

Library

Buscá: Google Sheets API

Click → Enable

✔️ Esto es obligatorio, sin esto nada funciona.

🔐 FASE 3 — Crear la Service Account (CLAVE)

Esto NO es tu mail personal.
Esto es el “usuario técnico” de la app.

3.1 Crear Service Account

IAM & Admin

Service Accounts

Create Service Account

Datos:

Name: fastapi-sheets-sa

ID: automático

Description: opcional

→ Create and Continue

3.2 Permisos (importante)

En “Grant this service account access”:

Role: Editor (simple y suficiente)

→ Continue
→ Done

🪪 FASE 4 — Generar la clave JSON (credenciales)

En Service Accounts

Click en la cuenta recién creada

Tab Keys

Add Key

Create new key

Tipo: JSON

Create

📥 Se descarga un archivo tipo:

fastapi-sheets-sa-123abc.json


⚠️ ESTE ARCHIVO ES SECRETO
⚠️ NO se commitea nunca

📊 FASE 5 — Crear el Google Sheet

Entrá a https://drive.google.com

New → Google Sheets

Nombre: Usuarios

Primera hoja:

Nombre: users

Ejemplo de contenido:

id	nombre	edad	email
1	Ale	30	a@a.com
🤝 FASE 6 — Compartir el Sheet con la Service Account

ESTE PASO ES EL MÁS OLVIDADO.

Abrí el Sheet

Share

Copiá del JSON:

"client_email": "fastapi-sheets-sa@xxxx.iam.gserviceaccount.com"


Pegalo como usuario

Permiso: Editor

Share

📌 NO uses tu mail
📌 USÁ EXACTAMENTE el client_email

🆔 FASE 7 — Obtener el Spreadsheet ID

Desde la URL:

https://docs.google.com/spreadsheets/d/1ABCDEF123456/edit#gid=0


El ID es:

1ABCDEF123456

🧪 FASE 8 — Preparar el .env (local)

Abrí el JSON descargado y copiá TODO el contenido.

.env
SPREADSHEET_ID=1ABCDEF123456
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"..."}


⚠️ Todo en una sola línea
⚠️ Comillas dobles escapadas si hace falta

Ejemplo seguro:

GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'

🧠 FASE 9 — Código esperado (sanity check)

Esto tiene que funcionar:

creds = Credentials.from_service_account_info(
    json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")),
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)


Si falla acá → SIEMPRE es:

Sheet no compartido

Mail incorrecto

Proyecto equivocado

API no habilitada

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