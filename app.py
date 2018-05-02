import os
import hashlib
from flask import Flask, render_template, request, abort
from redis import Redis

app = Flask(__name__)
redis_client = Redis.from_url(os.environ['REDIS_URL'])


@app.route('/', methods=['GET', 'POST'])
def index():
    encr_text = request.form.get('encr')
    if request.method == 'POST' and encr_text:
        if len(encr_text) > 2000:
            abort(400)
        key = hashlib.sha224(encr_text.encode('utf-8')).hexdigest()
        redis_client.setex(key, encr_text, 3600 * 24 * 3)
        return key
    return render_template('index.html')


@app.route('/decode', methods=['POST'])
def decode():
    hash = request.form.get('hash')
    if hash:
        encr_text = redis_client.get(hash)
        if encr_text:
            redis_client.delete(hash)
            return encr_text
    abort(400)
