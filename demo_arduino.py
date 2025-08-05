#!/usr/bin/env python3
"""
Demo Arduino Simulator para Sauna de Calango
Simula dados do Arduino para testar a interface web sem hardware
"""

import time
import math
import random
import serial
from serial.tools.list_ports import comports
import threading
import sys

class ArduinoSimulator:
    def __init__(self, port_name="COM_VIRTUAL", baud_rate=9600):
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.running = False
        self.start_time = None
        
        # Parâmetros da simulação
        self.base_temp = 25.0  # Temperatura inicial
        self.target_temp = 45.0  # Temperatura alvo
        self.heating_rate = 0.02  # Taxa de aquecimento por segundo
        self.noise_amplitude = 0.5  # Amplitude do ruído
        
    def simulate_temperature_data(self):
        """Simula dados realistas de temperatura"""
        if not self.start_time:
            self.start_time = time.time()
            
        current_time = time.time()
        elapsed_ms = int((current_time - self.start_time) * 1000)
        elapsed_seconds = elapsed_ms / 1000.0
        
        # Simular aquecimento gradual com curva exponencial
        progress = 1 - math.exp(-elapsed_seconds * 0.01)
        current_temp = self.base_temp + (self.target_temp - self.base_temp) * progress
        
        # Adicionar ruído realista
        noise = random.uniform(-self.noise_amplitude, self.noise_amplitude)
        current_temp += noise
        
        # Adicionar variações periódicas (simulando oscilações do controle)
        oscillation = 0.3 * math.sin(elapsed_seconds * 0.1)
        current_temp += oscillation
        
        # Limitar temperatura máxima
        current_temp = min(current_temp, self.target_temp + 2.0)
        
        return elapsed_ms, current_temp, self.target_temp
    
    def start_simulation(self):
        """Inicia a simulação de dados"""
        self.running = True
        self.start_time = time.time()
        
        print(f"🦎 Simulador Arduino iniciado!")
        print(f"   Porta Virtual: {self.port_name}")
        print(f"   Baud Rate: {self.baud_rate}")
        print(f"   Temperatura inicial: {self.base_temp}°C")
        print(f"   Temperatura alvo: {self.target_temp}°C")
        print("   Pressione Ctrl+C para parar\n")
        
        try:
            while self.running:
                time_ms, current_temp, target_temp = self.simulate_temperature_data()
                
                # Formato esperado pelo app.py: "tempo_ms;temperatura_atual;temperatura_desejada"
                data_line = f"{time_ms};{current_temp:.2f};{target_temp:.2f}"
                
                print(f"[{time_ms/1000:.1f}s] Temp: {current_temp:.2f}°C | Alvo: {target_temp:.2f}°C")
                
                # Simular envio via serial (apenas para debug)
                # Em uma implementação real, isso seria enviado via porta serial
                
                # Aguardar próxima leitura (simulando frequência do Arduino)
                time.sleep(1.0)  # 1 leitura por segundo
                
        except KeyboardInterrupt:
            print("\n🛑 Simulação interrompida pelo usuário")
            self.stop_simulation()
    
    def stop_simulation(self):
        """Para a simulação"""
        self.running = False
        print("✅ Simulação finalizada")

class VirtualSerial:
    """Classe para simular porta serial virtual"""
    
    def __init__(self, port_name="COM_VIRTUAL"):
        self.port_name = port_name
        self.simulator = ArduinoSimulator(port_name)
        self.is_open = False
        self.data_queue = []
        self.thread = None
        
    def open(self):
        """Abre a porta serial virtual"""
        self.is_open = True
        self.thread = threading.Thread(target=self._generate_data)
        self.thread.daemon = True
        self.thread.start()
        print(f"📡 Porta serial virtual {self.port_name} aberta")
        
    def close(self):
        """Fecha a porta serial virtual"""
        self.is_open = False
        if self.thread:
            self.thread.join(timeout=1)
        print(f"🔒 Porta serial virtual {self.port_name} fechada")
        
    def readline(self):
        """Lê uma linha de dados simulados"""
        while self.is_open and not self.data_queue:
            time.sleep(0.1)  # Aguardar dados
            
        if self.data_queue:
            return self.data_queue.pop(0)
        return b""
        
    def _generate_data(self):
        """Gera dados em thread separada"""
        simulator = ArduinoSimulator()
        simulator.start_time = time.time()
        
        while self.is_open:
            time_ms, current_temp, target_temp = simulator.simulate_temperature_data()
            data_line = f"{time_ms};{current_temp:.2f};{target_temp:.2f}\n"
            self.data_queue.append(data_line.encode('utf-8'))
            time.sleep(1.0)  # 1Hz

def monkey_patch_serial():
    """Aplica monkey patch para simular Arduino"""
    original_Serial = serial.Serial
    original_comports = comports
    
    def mock_comports():
        """Simula lista de portas COM com Arduino virtual"""
        return [type('obj', (object,), {
            'device': 'COM_VIRTUAL',
            'description': 'CH340 Virtual Arduino Simulator',
            'hwid': 'USB VID:PID=1A86:7523'
        })]
    
    def mock_Serial(port, *args, **kwargs):
        """Simula Serial do Arduino"""
        if port == 'COM_VIRTUAL':
            virtual_serial = VirtualSerial(port)
            virtual_serial.open()
            return virtual_serial
        else:
            return original_Serial(port, *args, **kwargs)
    
    # Aplicar patches
    serial.Serial = mock_Serial
    serial.tools.list_ports.comports = mock_comports
    
    print("🔧 Monkey patch aplicado - Arduino virtual ativo")

def main():
    """Função principal para demonstração"""
    print("🦎 DEMO - Sauna de Calango Arduino Simulator")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--patch':
        print("🔧 Modo Patch - Modificando comportamento do serial")
        monkey_patch_serial()
        print("✅ Execute 'python app.py' em outro terminal")
        print("   A interface web detectará o Arduino virtual")
        
        # Manter script rodando
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Demo finalizada")
    else:
        print("🎮 Modo Standalone - Simulação independente")
        simulator = ArduinoSimulator()
        simulator.start_simulation()

if __name__ == "__main__":
    print("\n📋 Opções de uso:")
    print("   python demo_arduino.py           # Simulação standalone")
    print("   python demo_arduino.py --patch   # Patch para app.py")
    print()
    
    main()