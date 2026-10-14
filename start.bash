#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_DIR="$BACKEND_DIR/scripture_env"

if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
  echo "Python environment not found at: $VENV_DIR"
  echo "Create it with: python3 -m venv backend/scripture_env"
  exit 1
fi

cd "$BACKEND_DIR"
source "$VENV_DIR/bin/activate"

if ! python -c 'import os; from dotenv import load_dotenv; load_dotenv(); key = os.getenv("OPENAI_API_KEY", ""); raise SystemExit(0 if key and key != "your-api-key" else 1)'; then
  echo "OPENAI_API_KEY is not configured."
  echo "Add it to backend/.env as: OPENAI_API_KEY=your-api-key"
  exit 1
fi

echo "Starting backend at http://localhost:8000"
exec python -m uvicorn app.main:app --reload
