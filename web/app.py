from flask import Flask
from flask import render_template
from flask import request
import re

app = Flask(__name__)

def validate_strings(tiempo,distancia,topic,email):
    
    # Verify time string
    time_regex = r"^[0-9]+$"
    if not re.fullmatch(time_regex, tiempo):
        return False
    elif 5 > int(tiempo) > 200: 
        return False

    # Verify email string
    email_regex = r"^\S+@\S+\.\S+$"
    if not re.fullmatch(email_regex, email):
        return False

    # Verify distance String 
    distance_regex = r"^[0-9]+$"
    if not re.fullmatch(distance_regex, distancia):
        return False
    elif 5 > int(distancia) > 200: 
        return False

    topic_regex = r"^\w+/*\w+$"
    if not re.fullmatch(topic_regex, topic) or len(topic) > 30:
        return False
    return True 

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/index')
def index(name=None):
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


    if validate_strings(tiempo,distancia,topic,email):
        return "<p> Successful </p>"
    return "<p> Not valid parameters </p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)