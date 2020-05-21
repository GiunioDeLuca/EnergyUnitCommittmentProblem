from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from optimise import optimAlg
import os
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = "segreta"
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if not request.is_json:
            return jsonify(message='json file is required'), 406
        else:
            solut, status = optimAlg(request.json)
            emit('event', {'inp': request.json, 'sol': solut}, broadcast=True, namespace='/test')
            return jsonify(solut), status

if __name__ == '__main__':
    if os.environ.get('AM_I_IN_DOCKER_CONTAINER', False):
        print(os.environ.get('host.docker.internal'))
        socketio.run(app, log_output=True, debug=True, port=8888, host='0.0.0.0')
    else:
        socketio.run(app, log_output=True, debug=True, port=8888)
