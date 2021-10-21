from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'EEE3095S Tutorial 6: By Luc van den Handel (VHNLUC001) and Sabrina Mackay (MCKSAB001) :)'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
