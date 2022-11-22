from flask import Flask
from flask import render_template
from flask import request
import re

app = Flask(__name__)

#@app.route('/', defaults={'path': ''})
#@app.route('/<path:path>')
#def catch_all(path):
#    return 'You want path: %s' % path

#@app.route("/")
#def hello_world():
#    return render_template('index.html')

def validate_strings(tiempo,distancia,topic,email):
    #re.search('\d', tiempo)
    time_regex = r"^\S+@\S+\.\S+$"
    if not re.fullmatch(time_regex, tiempo):
        return False

    email_regex = r"^\S+@\S+\.\S+$"
    if not re.fullmatch(email_regex, email):
        return False

    

@app.route('/index')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/set_parameters')
def set_parameters():
    tiempo = request.args.get('tiempo')
    distancia = request.args.get('distancia')
    topic = request.args.get('topic')
    email = request.args.get('correo')
    print (tiempo)
    print(distancia)
    print(topic)
    print(email)
    return "<p> Suscessful </p>"