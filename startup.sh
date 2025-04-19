#!/bin/bash
echo "=== ENVIRONMENT VARIABLES ===" >&2
env >&2
echo "=== STARTING GUNICORN ===" >&2
echo "🚀 Gunicorn 起動開始"
gunicorn --config gunicorn.py main:app