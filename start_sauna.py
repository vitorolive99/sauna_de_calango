#!/usr/bin/env python3
"""
Script de Inicialização Rápida - Sauna de Calango
Facilita o processo de instalação e execução da interface web
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

class SaunaStarter:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dependencies_installed = False
        
    def print_banner(self):
        """Exibe banner do projeto"""
        banner = """
    🦎 SAUNA DE CALANGO - CTmax Monitor
    ════════════════════════════════════════
    
    Sistema de Monitoramento de Temperatura
    para Experimentos de Critical Thermal Maximum
    
    Versão: 2.0 (Interface Web)
    Desenvolvido para pesquisa científica
    
    ════════════════════════════════════════
    """
        print(banner)
    
    def check_python_version(self):
        """Verifica versão do Python"""
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ é necessário")
            print(f"   Versão atual: {sys.version}")
            return False
        
        print(f"✅ Python {sys.version.split()[0]} detectado")
        return True
    
    def check_dependencies(self):
        """Verifica se as dependências estão instaladas"""
        required_packages = ['flask', 'flask_socketio', 'serial']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package} instalado")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} não encontrado")
        
        return len(missing_packages) == 0, missing_packages
    
    def install_dependencies(self):
        """Instala dependências necessárias"""
        print("\n🔧 Instalando dependências...")
        
        # Verificar se pipenv está disponível
        try:
            subprocess.run(['pipenv', '--version'], 
                         capture_output=True, check=True)
            print("📦 Usando Pipenv...")
            subprocess.run(['pipenv', 'install'], check=True)
            print("✅ Dependências instaladas via Pipenv")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("📦 Pipenv não encontrado, usando pip...")
            
            try:
                packages = ['flask', 'flask-socketio', 'python-socketio', 'pyserial']
                for package in packages:
                    print(f"   Instalando {package}...")
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                 check=True, capture_output=True)
                
                print("✅ Dependências instaladas via pip")
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro na instalação: {e}")
                return False
    
    def create_directories(self):
        """Cria diretórios necessários"""
        directories = ['Experiencias', 'static/css', 'static/js', 'static/images', 'templates']
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
        print("✅ Diretórios verificados/criados")
    
    def check_arduino_connection(self):
        """Verifica conexão com Arduino"""
        try:
            import serial.tools.list_ports as ports
            
            arduino_ports = [p for p in ports.comports() 
                           if 'CH340' in p.description or 'Arduino' in p.description]
            
            if arduino_ports:
                print(f"✅ Arduino detectado em: {arduino_ports[0].device}")
                return True
            else:
                print("⚠️  Arduino não detectado")
                print("   Você pode usar o modo demonstração")
                return False
                
        except ImportError:
            print("⚠️  Não foi possível verificar portas seriais")
            return False
    
    def start_application(self, demo_mode=False):
        """Inicia a aplicação"""
        print(f"\n🚀 Iniciando Sauna de Calango...")
        
        if demo_mode:
            print("🎮 Modo Demonstração Ativado")
            # Importar e aplicar patch do demo
            try:
                import demo_arduino
                demo_arduino.monkey_patch_serial()
                print("✅ Arduino virtual configurado")
            except ImportError:
                print("❌ Arquivo demo_arduino.py não encontrado")
                return False
        
        try:
            # Aguardar um momento e abrir navegador
            def open_browser():
                time.sleep(2)
                webbrowser.open('http://localhost:5000')
                print("🌐 Navegador aberto em http://localhost:5000")
            
            import threading
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # Iniciar aplicação Flask
            print("🖥️  Servidor web iniciando...")
            print("   Acesse: http://localhost:5000")
            print("   Pressione Ctrl+C para parar\n")
            
            # Importar e executar app
            import app
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar aplicação: {e}")
            return False
    
    def interactive_menu(self):
        """Menu interativo para o usuário"""
        while True:
            print("\n📋 MENU PRINCIPAL")
            print("1. 🚀 Iniciar com Arduino conectado")
            print("2. 🎮 Iniciar modo demonstração (sem Arduino)")
            print("3. 🔧 Instalar/atualizar dependências")
            print("4. 📊 Verificar sistema")
            print("5. 📖 Mostrar instruções")
            print("6. ❌ Sair")
            
            choice = input("\nEscolha uma opção (1-6): ").strip()
            
            if choice == '1':
                if self.check_arduino_connection():
                    self.start_application(demo_mode=False)
                else:
                    print("\n❌ Arduino não detectado!")
                    print("   Conecte o Arduino ou use o modo demonstração (opção 2)")
                    
            elif choice == '2':
                self.start_application(demo_mode=True)
                
            elif choice == '3':
                self.install_dependencies()
                
            elif choice == '4':
                self.system_check()
                
            elif choice == '5':
                self.show_instructions()
                
            elif choice == '6':
                print("👋 Até logo!")
                break
                
            else:
                print("❌ Opção inválida. Tente novamente.")
    
    def system_check(self):
        """Verificação completa do sistema"""
        print("\n🔍 VERIFICAÇÃO DO SISTEMA")
        print("-" * 30)
        
        # Python
        python_ok = self.check_python_version()
        
        # Dependências
        deps_ok, missing = self.check_dependencies()
        if not deps_ok:
            print(f"❌ Dependências faltando: {', '.join(missing)}")
        
        # Diretórios
        self.create_directories()
        
        # Arduino
        arduino_ok = self.check_arduino_connection()
        
        # Arquivos essenciais
        essential_files = ['app.py', 'templates/index.html', 'static/js/app.js']
        files_ok = True
        
        for file_path in essential_files:
            if (self.project_root / file_path).exists():
                print(f"✅ {file_path} encontrado")
            else:
                print(f"❌ {file_path} não encontrado")
                files_ok = False
        
        # Resumo
        print("\n📋 RESUMO DA VERIFICAÇÃO")
        print(f"   Python: {'✅' if python_ok else '❌'}")
        print(f"   Dependências: {'✅' if deps_ok else '❌'}")
        print(f"   Arquivos: {'✅' if files_ok else '❌'}")
        print(f"   Arduino: {'✅' if arduino_ok else '⚠️ '}")
        
        if python_ok and deps_ok and files_ok:
            print("\n🎉 Sistema pronto para uso!")
        else:
            print("\n⚠️  Corrija os problemas antes de continuar")
    
    def show_instructions(self):
        """Mostra instruções detalhadas"""
        instructions = """
    📖 INSTRUÇÕES DE USO
    ═══════════════════════
    
    🔌 CONEXÃO DO ARDUINO:
       1. Conecte o Arduino via USB
       2. Verifique se os drivers CH340 estão instalados
       3. O sistema detectará automaticamente a porta
    
    🚀 EXECUTAR O SISTEMA:
       1. Execute: python start_sauna.py
       2. Escolha a opção 1 (com Arduino) ou 2 (demo)
       3. Aguarde a interface abrir no navegador
       4. Acesse: http://localhost:5000
    
    🎛️ USANDO A INTERFACE:
       • Botão "Iniciar Experimento": Inicia coleta de dados
       • Botão "Parar Experimento": Para a coleta
       • Gráfico: Mostra temperaturas em tempo real
       • Histórico: Lista todos os experimentos salvos
    
    📊 ATALHOS DE TECLADO:
       • Ctrl + S: Iniciar experimento
       • Ctrl + X: Parar experimento
    
    📁 ARQUIVOS GERADOS:
       • Experiencias/CTmaxN - DD-MM-YYYY.csv
       • Formato: Tempo(ms);Temperatura(C);TemperaturaDesejada(C)
    
    🐛 SOLUÇÃO DE PROBLEMAS:
       • Arduino não detectado: Verificar conexão USB e drivers
       • Porta 5000 ocupada: Fechar outros serviços na porta
       • Interface não abre: Verificar console para erros
       • Dados não aparecem: Verificar formato de dados do Arduino
    
    💡 DICAS:
       • Use modo demonstração para testar sem hardware
       • Mantenha o Arduino conectado durante todo o experimento
       • Faça backup dos arquivos CSV importantes
       • Monitore a temperatura para evitar superaquecimento
    
    ═══════════════════════
        """
        print(instructions)
    
    def run(self):
        """Execução principal"""
        self.print_banner()
        
        # Verificação inicial rápida
        if not self.check_python_version():
            input("Pressione Enter para sair...")
            return
        
        # Verificar dependências básicas
        deps_ok, missing = self.check_dependencies()
        
        if not deps_ok:
            print(f"\n🔧 Instalando dependências faltantes: {', '.join(missing)}")
            if self.install_dependencies():
                print("✅ Dependências instaladas com sucesso!")
            else:
                print("❌ Falha na instalação. Instale manualmente:")
                print("   pip install flask flask-socketio pyserial")
                input("Pressione Enter para sair...")
                return
        
        # Menu interativo
        self.interactive_menu()

def main():
    """Função principal"""
    starter = SaunaStarter()
    starter.run()

if __name__ == "__main__":
    main()