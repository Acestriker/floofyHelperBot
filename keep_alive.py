from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "01000011 01101001 01100100 01100101 01101100 00100000 01101001 01110011 00100000 01100001 00100000 01100110 01110101 01110010 01110010 01111001 00100000 00111011 00101001"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()