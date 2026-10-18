# 🚀 Cómo ejecutar Finance (PC con Windows y servidor Ubuntu en GCP)

La app tiene dos partes:

| Parte | Archivo | Para qué sirve |
|---|---|---|
| Analizador (lo que ya tenías) | `buscar_acciones.py`, `dashboard.py`, `analizar_personalizado.py`… | Genera recomendaciones y las guarda en `finance.db` |
| **Interfaz web (nuevo)** | `web_app.py` + carpetas `templates/` y `static/` | Ver recomendaciones, marcar en cuáles invertiste y ver cuánto vas ganando/perdiendo |
| Análisis automático (nuevo) | `analisis_programado.py` | Corre el análisis sin hacer preguntas (lo usa el botón de la web y el cron del servidor) |
| Seguimiento de inversiones (nuevo) | `portfolio.py` | Tabla `investments` dentro de `finance.db` |

> ⚠️ Tu PC y el servidor tienen **cada uno su propio `finance.db`**. Lo que marques en el servidor no aparece en tu PC y viceversa. Usa el **servidor** como el lugar "oficial" para registrar tus inversiones.

---

## 1. En tu PC (Windows)

Abre **PowerShell** en la carpeta del proyecto:

```powershell
cd C:\laragon\www\Finance

# Solo la primera vez: crea .venv e instala dependencias (flask, waitress, yfinance, pandas…)
.\instalar_windows.bat

# Abrir la interfaz web (se abre sola en el navegador en http://127.0.0.1:5000)
.\iniciar_web.bat
```

Equivalente a mano (sin los .bat):

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
.venv\Scripts\python.exe web_app.py
```

- En tu PC no hace falta contraseña (la app solo escucha en `127.0.0.1`, nadie más puede entrar).
- Para detenerla: `Ctrl + C` en la ventana negra.
- Tus scripts de siempre siguen funcionando: `.venv\Scripts\python.exe buscar_acciones.py`
  (también corregí `ejecutar_analisis.bat` y `ejecutar_dashboard.bat`, que apuntaban a otro `.venv` en `C:\laragon\www\scripts`).

---

## 2. Subir el código a GitHub (desde tu PC)

`finance.db` ya no debe ir en git (cada equipo tiene su propia base y si no, `git pull` chocaría en el servidor):

```powershell
cd C:\laragon\www\Finance
git rm --cached finance.db
git add .
git commit -m "Interfaz web, seguimiento de inversiones y despliegue"
git push
```

---

## 3. En el servidor (Ubuntu en GCP)

### 3.1 Abrir el puerto 80 en el firewall de GCP

Opción fácil: **Consola de GCP → Compute Engine → Instancias de VM → tu instancia → Editar →**
marca **"Permitir tráfico HTTP"** (y "HTTPS" si luego pondrás certificado) → Guardar.

Opción con comandos (desde Cloud Shell o tu PC con `gcloud`). Cambia `MI-VM` y la zona por las tuyas:

```bash
gcloud compute instances add-tags MI-VM --tags=http-server,https-server --zone=us-central1-a
# Solo si tu proyecto no tiene ya la regla "default-allow-http":
gcloud compute firewall-rules create default-allow-http --allow=tcp:80 --target-tags=http-server
gcloud compute firewall-rules create default-allow-https --allow=tcp:443 --target-tags=https-server
```

### 3.2 Instalar la app (por SSH en la VM)

```bash
cd ~
git clone https://github.com/adriantg99/Finance.git
cd Finance
bash deploy/instalar_servidor.sh
```

> Si el repositorio es **privado**, `git clone` te pedirá usuario y contraseña: la contraseña es un
> *Personal Access Token* de GitHub (Settings → Developer settings → Tokens), no tu contraseña normal.

El script te pide la **contraseña para entrar a la web**, y deja todo listo:
- servicio `finance-web` que arranca solo cuando se prende el servidor y se reinicia si falla,
- nginx en el puerto 80,
- análisis automático de lunes a viernes a las 15:00 (hora de Hermosillo) con evaluación de las recomendaciones vencidas.

Al terminar muestra la dirección: **`http://IP_EXTERNA`**. Ábrela desde cualquier lugar (celular incluido).

### 3.3 (Opcional) Llevar al servidor las recomendaciones que ya tienes en tu PC

Desde tu PC (PowerShell, con `gcloud` instalado):

```powershell
gcloud compute scp C:\laragon\www\Finance\finance.db MI-VM:~/Finance/finance.db --zone=us-central1-a
```

Y en el servidor: `sudo systemctl restart finance-web`.

### 3.4 Comandos útiles en el servidor

```bash
sudo systemctl status finance-web        # ¿está corriendo?
journalctl -u finance-web -f             # ver errores/registro en vivo
sudo systemctl restart finance-web       # reiniciar
tail -f ~/Finance/logs/analisis.log      # registro del análisis automático
crontab -l                               # ver la programación del análisis
nano ~/Finance/.env                      # cambiar contraseña (luego reinicia el servicio)

# Después de hacer git push con cambios desde tu PC:
cd ~/Finance && bash deploy/actualizar.sh

# Correr el análisis a mano:
cd ~/Finance && .venv/bin/python analisis_programado.py --rapido
```

### 3.5 IP fija (recomendado)

Por defecto la IP externa de GCP puede cambiar si apagas la VM. Para fijarla:
**VPC network → Direcciones IP → (tu IP externa) → "Promover a estática"**, o:

```bash
gcloud compute addresses create finance-ip --addresses=TU_IP_EXTERNA --region=us-central1
```

### 3.6 HTTPS (muy recomendado)

Con `http://` la contraseña viaja sin cifrar. Para tener `https://` necesitas un dominio
(sirve uno gratis de [duckdns.org](https://www.duckdns.org) apuntando a tu IP). Luego, en el servidor:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo sed -i 's/server_name _;/server_name TU-DOMINIO.duckdns.org;/' /etc/nginx/sites-available/finance
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d TU-DOMINIO.duckdns.org
sed -i 's/^COOKIE_SECURE=.*/COOKIE_SECURE=1/' ~/Finance/.env && sudo systemctl restart finance-web
```

---

## 4. Problemas comunes

| Síntoma | Solución |
|---|---|
| La página no abre desde fuera | Revisa el paso 3.1 (firewall) y `sudo systemctl status nginx finance-web` |
| "502 Bad Gateway" | La app de Python no corre: `journalctl -u finance-web -n 50` |
| "Precio no disponible" | Yahoo Finance limitó las consultas; espera 1–2 minutos y presiona "Actualizar precios" |
| El análisis completo tarda mucho | Normal con ~200 acciones (10–25 min). Usa el análisis rápido o reduce `MIS_ACCIONES` en `config.py` |
| Olvidé la contraseña | En el servidor: `nano ~/Finance/.env`, cambia `FINANCE_PASSWORD` y `sudo systemctl restart finance-web` |
| Bloqueado por intentos | Tras 5 contraseñas incorrectas se bloquea 5 minutos esa IP |
