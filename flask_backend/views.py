from flask import make_response
from flask_backend.app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    return make_response("Hello World")
