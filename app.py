import serial
from serial.tools.list_ports import comports
import csv
from datetime import datetime
import os
import json
import threading
import time
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

# Inicialização da aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sauna_de_calango_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Variáveis globais para controle do experimento
experiment_running = False
experiment_thread = None
current_data = {}

# Função para encontrar a porta serial do Arduino
def find_arduino_port():
    usb = 'CH340'  # Descrição do dispositivo Arduino
    
    arduino_ports = [
        p.device
        for p in comports()
        if usb in p.description  # Verifica se a descrição do dispositivo contém 'Arduino'
    ]
    
    if not arduino_ports:
        raise IOError("Nenhum Arduino encontrado.")
    
    if len(arduino_ports) > 1:
        print("Vários Arduinos encontrados. Usando o primeiro encontrado:", arduino_ports[0])
    
    return arduino_ports[0]

# Função para executar o experimento em thread separada
def run_experiment():
    global experiment_running, current_data
    arquivo = "ultima_exp.txt"
    
    try:
        # Encontra a porta serial do Arduino
        arduino_port = find_arduino_port()
        print("Porta serial do Arduino encontrada:", arduino_port)
        
        # Lê o numero da ultima experiência
        with open(arquivo, "r") as file:
            last_experience = file.read().strip()

        # Se o arquivo estiver vazio, cria a experiência 0
        if not last_experience:
            last_experience = 0
            
        experience_code = int(last_experience) + 1
        execution_date = datetime.now().strftime("%d-%m-%Y")
        
        # Cria a pasta Experiencias se não existir
        if not os.path.exists("Experiencias"):
            os.makedirs("Experiencias")
            
        file_path = f"Experiencias/CTmax{experience_code} - {execution_date}.csv"
        
        # Salva o código da experiência no arquivo ultima_exp.txt
        with open(arquivo, "w") as file:
            file.write(str(experience_code))
        
        # configuração da porta serial
        baud_rate = 9600
        ser = serial.Serial(arduino_port, baud_rate)

        # Cria um arquivo CSV para salvar os dados
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Tempo(ms)", "Temperatura (C)", "Temperatura Desejada (C)"])

            while experiment_running:
                try:
                    line = ser.readline().decode().strip()
                    data = line.split(";")
                    
                    if len(data) >= 3:
                        current_data = {
                            'timestamp': datetime.now().isoformat(),
                            'tempo_ms': data[0],
                            'temperatura_atual': data[1],
                            'temperatura_desejada': data[2],
                            'experience_code': experience_code
                        }
                        
                        # Envia dados em tempo real via SocketIO
                        socketio.emit('new_data', current_data)
                        
                        writer.writerow(data)
                        file.flush()
                        
                except Exception as e:
                    print(f"Erro ao ler dados: {e}")
                    continue
                    
        ser.close()

    except Exception as e:
        print("Erro", str(e))
        experiment_running = False
        socketio.emit('experiment_error', {'error': str(e)})

# Rotas Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_experiment', methods=['POST'])
def start_experiment():
    global experiment_running, experiment_thread
    
    if not experiment_running:
        experiment_running = True
        experiment_thread = threading.Thread(target=run_experiment)
        experiment_thread.start()
        return jsonify({'status': 'success', 'message': 'Experimento iniciado'})
    else:
        return jsonify({'status': 'error', 'message': 'Experimento já está em andamento'})

@app.route('/api/stop_experiment', methods=['POST'])
def stop_experiment():
    global experiment_running
    experiment_running = False
    return jsonify({'status': 'success', 'message': 'Experimento parado'})

@app.route('/api/status')
def get_status():
    return jsonify({
        'running': experiment_running,
        'current_data': current_data
    })

@app.route('/api/experiments')
def get_experiments():
    experiments = []
    if os.path.exists("Experiencias"):
        for filename in os.listdir("Experiencias"):
            if filename.endswith('.csv'):
                file_path = os.path.join("Experiencias", filename)
                stat = os.stat(file_path)
                experiments.append({
                    'filename': filename,
                    'created': datetime.fromtimestamp(stat.st_ctime).strftime("%d/%m/%Y %H:%M:%S"),
                    'size': stat.st_size
                })
    return jsonify(experiments)

# Eventos SocketIO
@socketio.on('connect')
def on_connect():
    emit('status', {'running': experiment_running, 'current_data': current_data})

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)