# Tag generation

Данный проект представляет собой систему тегирования видео на основе видеоконтента, названия и описания видео

Структура проекта:

- **flaskapp/**
  - Project front-end
- **ml/**
  - Папка, содержащая алгоритмы ML (speech2text, video2text, spellcast, classification)
- **main.py**
  - Файл запуска приложения.
- **utils.py**
  - Файл со вспомогательными функциями.
- **requirements.txt**
  - Файл, содержащий список зависимостей Python, необходимых для запуска проекта.

## Запуск проекта

Чтобы запустить проект, выполните следующие шаги:

### **Для локальной разработки**
1. Убедитесь, что у вас установлен Python версии 3.10 для стабильной работы.
2. Установите инструмент для создания изолированной среды Python 
`pip install virtualenv`
`pip install virtualenvwrapper-win`
3. Создайте изолированную среду в Python 
`python3 -m venv venv`
4. Активируйте созданную виртуальную среду
`venv\Scripts\activate` или `venv\Scripts\activate.bat`
5. Установите необходимые зависимости, выполнив следующую команду:
`pip install -r requirements.txt`
6. Запустите приложение, выполнив следующую команду:
`python main.py`
7. После этого ваше приложение будет доступно по адресу 
`http://127.0.0.1:8000/`

## Проблемы с установкой
Могут возникнуть проблемы с установкой библиотеки torch.
Чтобы исправить это:
1. В терминале выполните команду:
- **pip uninstall torch**
2. Перейдите на официальный сайт библиотеки https://pytorch.org/
3. Выполните команду установки как предложено на сайте. Это может выглядить следующим образом:
- **pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118**
Могут возникнуть проблемы с установкой библиотеки ffmpeg
Чтобы исправить это:
1. Загрузите архив https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
2. Распакуйте скачанный архив в C:\ (у вас должно получиться примерно так: C:\ffmpeg)
3. Добавьте путь в переменные среды
3.1. Введите изменение системных переменных среды в строку поиска и нажмите изменение системных переменных среды
3.2. Нажмите кнопку "Переменые среды", кликните Path, кликните Создать и вставьте путь к папке bin (C:\ffmpeg\bin)
## Улучшение производительности
Установите совместимые CUDA и Cudnn

