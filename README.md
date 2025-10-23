# Medicación diaria para mis perros (Streamlit)

App muy simple que muestra, para **hoy**, qué pastillas y suplementos corresponden a cada perro.
Cada pastilla tiene su **propia fecha de inicio** y frecuencia (en días o meses).

## Ejecutar en local (abre el navegador)
1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Lanza la app:
   ```bash
   streamlit run app.py
   ```
   Streamlit abrirá tu navegador automáticamente en `http://localhost:8501`.

## Despliegue (link público para móvil)
1. Sube este repo a GitHub.
2. Entra en **Streamlit Community Cloud** → **New app**.
3. Conecta tu cuenta de GitHub, elige el repo, rama y `app.py`.
4. Pulsa **Deploy**. Obtendrás una URL pública.
   Puedes guardarla como acceso directo en tu smartphone para abrirla con un toque.

## Personalización
- Cambia los nombres de los perros desde la barra lateral.
- Edita `SCHEDULE` en `app.py` para añadir/quitar pastillas, cambiar fechas de inicio o frecuencias.
- Soportado:
  - `every_n_days`: frecuencia en días desde `start_date`.
  - `every_n_months`: frecuencia en meses desde `start_date`.
  - `note`: texto libre (ej. “media pastilla”).

## Notas
- La app **no pide fecha**: siempre usa la fecha actual del sistema del servidor.
- Si necesitas ver otra fecha puntualmente, se puede añadir soporte opcional de `?date=YYYY-MM-DD`.
