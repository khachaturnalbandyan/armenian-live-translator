#!/usr/bin/env bash
# Launcher: makes the CUDA 12 libraries that CTranslate2 needs visible, then runs the app.
# Usage: ./run.sh --list-devices   |   ./run.sh --device <name>   |   ./run.sh --input file.wav
set -euo pipefail
cd "$(dirname "$0")"

VENV="${VENV:-.venv}"
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "error: $VENV/bin/python not found. Create it with:" >&2
  echo "  python3 -m venv --system-site-packages $VENV && $VENV/bin/pip install -r requirements.txt" >&2
  exit 1
fi

SITE="$("$VENV/bin/python" -c 'import site; print(site.getsitepackages()[0])')"
CUDA_LIBS="$SITE/nvidia/cublas/lib:$SITE/nvidia/cudnn/lib:$SITE/nvidia/cuda_nvrtc/lib"
export LD_LIBRARY_PATH="$CUDA_LIBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

exec "$VENV/bin/python" main.py "$@"
