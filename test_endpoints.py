import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pehchan_webapp.settings')
django.setup()

from django.test import Client

c = Client()
print("GET /login/:", c.get('/login/').status_code)

try:
    resp = c.post('/login/', {'username': 'test', 'password': '123'})
    print("POST /login/:", resp.status_code)
except Exception as e:
    print("POST /login/ Error:", e)

try:
    resp = c.get('/')
    print("GET /:", resp.status_code)
except Exception as e:
    print("GET / Error:", e)
