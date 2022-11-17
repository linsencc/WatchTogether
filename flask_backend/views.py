from flask import render_template
from flask_backend.app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    # return make_response("Watch together")
    print('visit index')
    return render_template('socketio/index.html')
