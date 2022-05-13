import requests

from flask import Blueprint
from flask import request, url_for, render_template, jsonify, make_response
from flask import current_app as app


GENERATOR_URL = 'http://127.0.0.1:8080'


bp = Blueprint('view', __name__, static_folder='static', url_prefix='/gendemo')


@bp.route('/')
def root():
    return show_index()


@bp.route('/')
def show_index():
    return render_template('index.html')


@bp.route('/generate', methods=['GET', 'POST'])
def tag_text():
    text = str(request.values['text'])
    format_ = str(request.values.get('format', 'html'))

    # TODO
    #req = requests.get(GENERATOR_URL, data={ 'text': text })
    #response = req.text
    response = 'Terve'
    return render_template('response.html', **locals())
