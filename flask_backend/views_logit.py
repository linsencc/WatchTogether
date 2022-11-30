from flask import render_template, make_response
from flask_backend.app import app
from flask_login import login_required


@app.route('/', methods=['GET', 'POST'])
def index():
    # return make_response("Watch together")
    return render_template('socketio/index.html')


@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    print('in test')
    return make_response({'data': {'a': 1, 'b': 2, 'c': 3}})
