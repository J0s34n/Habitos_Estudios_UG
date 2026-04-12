#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "from apps.ml_engine.predictor import entrenar_modelo; entrenar_modelo()"