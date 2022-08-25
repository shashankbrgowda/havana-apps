# Havana apps

A web application which contains below havana related utility applications.
- NI App
- NSI App

---

# Running locally

```

cd havana-apps

sudo apt install python3-pip

sudo apt install python3-venv

python3 -m venv ./venv

source venv/bin/activate

pip install -r requirements.txt

export FLASK_APP=run.py

flask run --host=0.0.0.0 --port=8080

```
