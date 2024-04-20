import serial
from serial.tools.list_ports import comports
import csv
from datetime import datetime


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

# Função para iniciar o programa
def start_program():
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

            while True:
                line = ser.readline().decode().strip()
                print(line)
                writer.writerow(line.split(";"))  # Escreve os dados no arquivo CSV
                file.flush()  # Força a gravação dos dados em disco

    except Exception as e:
        print("Erro", str(e))

if __name__ == "__main__":
    start_program()