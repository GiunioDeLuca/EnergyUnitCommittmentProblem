from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from optimiseDEBUG import checkfunc

app = Flask(__name__)
app.config['SECRET_KEY'] = "segreta"
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if not request.is_json():
            return jsonify(message='json file is required'), 406
        else:
            solut = checkfunc(request.json)
            if solut is not None:
                emit()
                return jsonify(solut)
            else:
                return jsonify(message='problem'), 406

