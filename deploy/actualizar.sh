#!/usr/bin/env bash
# Actualiza el código en el servidor después de hacer "git push" desde tu PC.
#   cd ~/Finance && bash deploy/actualizar.sh
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
git pull
.venv/bin/python -m pip install -r requirements.txt --quiet
sudo systemctl restart finance-web
echo "✅ Actualizado y reiniciado. Estado:"
systemctl --no-pager --lines=0 status finance-web
