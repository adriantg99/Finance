#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
#  Instalador de Finance en un servidor Ubuntu (probado para GCP Compute Engine)
#
#  Ejecútalo DESDE la carpeta del proyecto, con tu usuario normal (no root):
#      cd ~/Finance
#      bash deploy/instalar_servidor.sh
#
#  Qué hace:
#    1. Instala python3-venv, nginx y dependencias del sistema
#    2. Crea el entorno virtual .venv e instala requirements.txt
#    3. Crea .env (te pide la contraseña si no existe)
#    4. Crea el servicio systemd "finance-web" (arranca solo al prender el servidor)
#    5. Configura nginx en el puerto 80 -> app en 127.0.0.1:5000
#    6. Programa el análisis automático diario con cron (L-V 15:00 hora Hermosillo)
#  Puedes volver a ejecutarlo sin problema (por ejemplo después de un git pull).
# ═══════════════════════════════════════════════════════════════════════════
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_USER="$(id -un)"
SERVICE=finance-web
PORT=5000

if [ "$APP_USER" = "root" ]; then
  echo "❌ Ejecuta este script con tu usuario normal (sin sudo). Él pedirá sudo cuando lo necesite."
  exit 1
fi

echo "▶ Carpeta del proyecto: $APP_DIR  (usuario: $APP_USER)"

echo "▶ [1/6] Paquetes del sistema..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-venv python3-pip nginx git

echo "▶ [2/6] Entorno virtual y dependencias de Python..."
cd "$APP_DIR"
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
mkdir -p logs

echo "▶ [3/6] Archivo .env..."
if [ ! -f .env ]; then
  cp .env.example .env
fi
if ! grep -qE '^FINANCE_PASSWORD=.+' .env; then
  while true; do
    read -r -s -p "   Escribe la contraseña para entrar a la web: " P1; echo
    read -r -s -p "   Repítela: " P2; echo
    [ -n "$P1" ] && [ "$P1" = "$P2" ] && break
    echo "   No coinciden o está vacía, intenta de nuevo."
  done
  P_ESC=$(printf '%s' "$P1" | sed 's/[&|\\]/\\&/g')
  sed -i "s|^FINANCE_PASSWORD=.*|FINANCE_PASSWORD=${P_ESC}|" .env
fi
sed -i "s|^HOST=.*|HOST=127.0.0.1|; s|^PORT=.*|PORT=${PORT}|" .env
chmod 600 .env

echo "▶ [4/6] Servicio systemd ($SERVICE)..."
sudo tee /etc/systemd/system/${SERVICE}.service >/dev/null <<EOF
[Unit]
Description=Finance - interfaz web de inversiones
After=network-online.target
Wants=network-online.target

[Service]
User=${APP_USER}
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/.venv/bin/python ${APP_DIR}/web_app.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE}
sudo systemctl restart ${SERVICE}

echo "▶ [5/6] nginx (puerto 80 -> 127.0.0.1:${PORT})..."
sudo tee /etc/nginx/sites-available/finance >/dev/null <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    client_max_body_size 2m;

    location / {
        proxy_pass http://127.0.0.1:${PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$remote_addr;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
    }
}
EOF
sudo ln -sf /etc/nginx/sites-available/finance /etc/nginx/sites-enabled/finance
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl reload nginx || sudo systemctl restart nginx

echo "▶ [6/6] Análisis automático (cron)..."
# El servidor de GCP está en UTC. 22:00 UTC = 15:00 en Hermosillo, después del cierre del mercado de EE. UU.
CRON_LINE="0 22 * * 1-5 cd ${APP_DIR} && ${APP_DIR}/.venv/bin/python analisis_programado.py >> ${APP_DIR}/logs/analisis.log 2>&1"
( crontab -l 2>/dev/null | grep -v 'analisis_programado.py' ; echo "$CRON_LINE" ) | crontab -

sleep 2
if systemctl is-active --quiet ${SERVICE}; then
  IP=$(curl -s -H "Metadata-Flavor: Google" \
       "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip" 2>/dev/null || true)
  echo
  echo "════════════════════════════════════════════════════════════════"
  echo " ✅ Listo. La app está corriendo."
  echo "    Abre:  http://${IP:-IP_EXTERNA_DE_TU_SERVIDOR}"
  echo "    (Si no abre, revisa que el firewall de GCP permita el puerto 80; ver DESPLIEGUE.md)"
  echo
  echo "    Ver estado:      sudo systemctl status ${SERVICE}"
  echo "    Ver logs:        journalctl -u ${SERVICE} -f"
  echo "    Reiniciar:       sudo systemctl restart ${SERVICE}"
  echo "════════════════════════════════════════════════════════════════"
else
  echo "❌ El servicio no arrancó. Revisa: journalctl -u ${SERVICE} -n 50"
  exit 1
fi
