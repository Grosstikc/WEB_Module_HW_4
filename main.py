from flask import Flask, render_template, request, redirect, url_for
import socket
import json
from datetime import datetime
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])  # Змінено назву функції
def login():  # Виправлено
    if request.method == 'POST':
        # Опущено для скорочення
        return redirect(url_for('index'))  # Виправлено
    return render_template('message.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        # Опущено для скорочення
        return redirect(url_for('index'))  # Виправлено
    return render_template('message.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Змінено на UDP
    server_socket.bind(('localhost', 5000))

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = json.loads(data.decode('utf-8'))
        print("Received message:", message)
        save_data(message)

def save_data(message):  
    try:
        with open('storage/data.json', 'r+') as file:
            # спроба прочитати та розібрати вже існуючий Json
            data = json.load(file)
            # Переконаємося, що data є словником, де ключ це строкове представлення datetime
            if not isinstance(data, dict):
                data = {}
            # Додаємо нове повіломлення
            data[str(datetime.now())] = message
            # Перемотуємо файл на початок
            file.seek(0)
            # Перезаписуємо файл з оновленим JSON
            json.dump(data, file)
            # Обрізаємо файл, якщо новий вміст коротший за попередній
            file.truncate()
    except FileNotFoundError:
        # Якщо файл не існує, створюємо новий і записуємо дані
        with open('storage/data.json', 'w') as file:
            json.dump({str(datetime.now()): message}, file)


if __name__ == '__main__':
    t1 = Thread(target=lambda: app.run(port=3000, debug=True, use_reloader=False))
    t2 = Thread(target=start_socket_server)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
