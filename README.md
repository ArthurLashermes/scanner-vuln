python3 -m venv venv
source venv/bin/activate
pip freeze > requirements.txt
export FLASK_APP=app/main.py