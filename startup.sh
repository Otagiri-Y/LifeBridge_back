#!/bin/bash
echo "🚀 Gunicorn 起動開始"

gunicorn --config gunicorn.py main:app