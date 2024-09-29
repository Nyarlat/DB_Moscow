import os

from flaskapp import app
from flask import render_template, make_response, request, Response, jsonify, json
import json
from utils import get_tags


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/api/video', methods=['POST'])
def post_video():
    try:
        # Получаем видеофайл
        video_file = request.files.get('video')

        if not video_file:
            return jsonify({"error": "Нет видеофайла"}), 400

        # Сохраняем видеофайл (опционально)
        video_file.save(f"./{video_file.filename}")

        # Получаем текстовые данные
        name = request.form.get('name')
        desc = request.form.get('desc')

        # Получаем теги, текст речи, описание видеоряда
        cath, a2t, v2t = get_tags(video_file.filename, name, desc)

        os.remove(f"./{video_file.filename}")

        respone = {
            "cath": cath,
            "a2t": a2t,
            "v2t": v2t,
        }

        return jsonify(respone), 200

    except Exception as e:
        print("error:", e)
        return str(e), 500


def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))


def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)
