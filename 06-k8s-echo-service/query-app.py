import requests
import json

requests.get("http://127.0.0.1:5000/", data=json.dumps({"test": "content"}), headers = { "Content-Type": "application/json" })
