import os

from flaskapp import app
import pandas as pd
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, send_file
import functools
import json
from utils import get_categories_mock


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/video', methods=['POST'])
def post_video():
    print(1)
    try:
        # Получаем видеофайл
        video_file = request.files.get('video')

        if not video_file:
            return jsonify({"error": "Нет видеофайла"}), 400

        # Сохраняем видеофайл (опционально)
        # video_file.save(f"./{video_file.filename}")

        # Получаем текстовые данные
        text1 = request.form.get('text1')
        text2 = request.form.get('text2')

        cath = get_categories_mock()

        a2t = "В названиях и описаниях к видео уже может содержаться некоторая информация о видеоконтенте, но часто информация не совсем релевантна или неполна. Поэтому важно научиться работать с видеорядом, извлекать важные или часто повторяющиеся сущности, которые можно соотнести со списком тегов. Можно пробовать суммаризировать видео или извлекать сущности из полного видеоряда. Немаловажную роль может играть аудиодорожка, которую можно преобразовать в текст и извлечь теги оттуда, но не забывайте учесть, что часть видео могут не содержать речи совсем или речь может не соответствовать видеоряду. Список тегов - это также текстовые данные, которые можно преобразовать в вектора или при желании - разметить под свои нужды."
        v2t = "На платформу RUTUBE ежедневно заливаются сотни тысяч видео, большая часть которых - это ugc контент, то есть видео от обычных пользователей. Часть контента - это популярные шоу, передачи, каналы, другой лицензионный контент. Чтобы упорядочить весь этот контент, необходимо создать систему тегирования видео, чтобы разделять их по категориям и подкатегориям. Причем система должна быть достаточно гибкой к обновлению списка тегов, широко и разнообразно покрывать контент. Такая система также улучшит рекомендательную систему, так как возможно будет рекомендовать контент из любимой категории пользователя, например."

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