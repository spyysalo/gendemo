import logging

import requests

from flask import Blueprint
from flask import request, url_for, render_template, jsonify, make_response
from flask import current_app as app


GENERATOR_URL = 'http://127.0.0.1:8005'


bp = Blueprint('view', __name__, static_folder='static', url_prefix='/gendemo')


@bp.route('/')
def root():
    return show_index()


@bp.route('/')
def show_index():
    return render_template('index.html')


@bp.route('/generate', methods=['GET', 'POST'])
def tag_text():
    prompt  = str(request.values['text'])
    max_length  = str(request.values.get('max_length'))
    temperature  = str(request.values.get('temperature'))

    params = {
        'text': prompt,
        'max_length': max_length,
        'temperature': temperature,
    }

    logging.warning(f'params: {params}')
    req = requests.get(GENERATOR_URL, params=params)
    response = req.text
    logging.warning(response)

    response = response.replace('\n', '<br>')

    return render_template('response.html', **locals())
