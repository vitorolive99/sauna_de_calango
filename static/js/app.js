// Sauna de Calango - JavaScript Principal
class SaunaCalango {
    constructor() {
        this.socket = null;
        this.chart = null;
        this.isConnected = false;
        this.experimentRunning = false;
        this.lastTemperature = null;
        
        // Dados para o gráfico
        this.chartData = {
            labels: [],
            temperatures: [],
            targets: []
        };
        
        // Elementos DOM
        this.elements = {
            startBtn: document.getElementById('startBtn'),
            stopBtn: document.getElementById('stopBtn'),
            connectionStatus: document.getElementById('connectionStatus'),
            currentTime: document.getElementById('currentTime'),
            experimentStatus: document.getElementById('experimentStatus'),
            experimentNumber: document.getElementById('experimentNumber'),
            currentTemp: document.getElementById('currentTemp'),
            targetTemp: document.getElementById('targetTemp'),
            timeMs: document.getElementById('timeMs'),
            experimentsTable: document.getElementById('experimentsTable'),
            alertModal: new bootstrap.Modal(document.getElementById('alertModal'))
        };
        
        this.init();
    }
    
    init() {
        this.initSocket();
        this.initChart();
        this.initEventListeners();
        this.updateTime();
        this.loadExperiments();
        
        // Atualizar horário a cada segundo
        setInterval(() => this.updateTime(), 1000);
        
        // Recarregar experimentos a cada 30 segundos
        setInterval(() => this.loadExperiments(), 30000);
    }
    
    initSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Conectado ao servidor');
            this.isConnected = true;
            this.updateConnectionStatus();
        });
        
        this.socket.on('disconnect', () => {
            console.log('Desconectado do servidor');
            this.isConnected = false;
            this.updateConnectionStatus();
        });
        
        this.socket.on('status', (data) => {
            this.experimentRunning = data.running;
            this.updateExperimentStatus();
            
            if (data.current_data && Object.keys(data.current_data).length > 0) {
                this.updateCurrentData(data.current_data);
            }
        });
        
        this.socket.on('new_data', (data) => {
            this.updateCurrentData(data);
            this.addDataToChart(data);
        });
        
        this.socket.on('experiment_error', (data) => {
            this.showAlert('Erro no Experimento', data.error, 'danger');
            this.experimentRunning = false;
            this.updateExperimentStatus();
        });
    }
    
    initChart() {
        const ctx = document.getElementById('temperatureChart').getContext('2d');
        
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.chartData.labels,
                datasets: [
                    {
                        label: 'Temperatura Atual (°C)',
                        data: this.chartData.temperatures,
                        borderColor: '#ff6b6b',
                        backgroundColor: 'rgba(255, 107, 107, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Temperatura Desejada (°C)',
                        data: this.chartData.targets,
                        borderColor: '#4ecdc4',
                        backgroundColor: 'rgba(78, 205, 196, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        borderDash: [5, 5],
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        borderColor: 'rgba(255, 255, 255, 0.2)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Tempo',
                            color: '#666'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Temperatura (°C)',
                            color: '#666'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        beginAtZero: false
                    }
                },
                animation: {
                    duration: 750,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    initEventListeners() {
        this.elements.startBtn.addEventListener('click', () => this.startExperiment());
        this.elements.stopBtn.addEventListener('click', () => this.stopExperiment());
        
        // Teclas de atalho
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                this.startExperiment();
            } else if (e.ctrlKey && e.key === 'x') {
                e.preventDefault();
                this.stopExperiment();
            }
        });
    }
    
    async startExperiment() {
        try {
            this.elements.startBtn.disabled = true;
            this.elements.startBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Iniciando...';
            
            const response = await fetch('/api/start_experiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.experimentRunning = true;
                this.updateExperimentStatus();
                this.clearChart();
                this.showAlert('Sucesso', data.message, 'success');
            } else {
                this.showAlert('Erro', data.message, 'danger');
            }
            
        } catch (error) {
            console.error('Erro ao iniciar experimento:', error);
            this.showAlert('Erro', 'Falha na comunicação com o servidor', 'danger');
        } finally {
            this.elements.startBtn.disabled = false;
            this.elements.startBtn.innerHTML = '<i class="fas fa-play me-2"></i>Iniciar Experimento';
        }
    }
    
    async stopExperiment() {
        try {
            this.elements.stopBtn.disabled = true;
            this.elements.stopBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Parando...';
            
            const response = await fetch('/api/stop_experiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.experimentRunning = false;
                this.updateExperimentStatus();
                this.showAlert('Sucesso', data.message, 'success');
                this.loadExperiments(); // Recarregar lista de experimentos
            } else {
                this.showAlert('Erro', data.message, 'danger');
            }
            
        } catch (error) {
            console.error('Erro ao parar experimento:', error);
            this.showAlert('Erro', 'Falha na comunicação com o servidor', 'danger');
        } finally {
            this.elements.stopBtn.disabled = false;
            this.elements.stopBtn.innerHTML = '<i class="fas fa-stop me-2"></i>Parar Experimento';
        }
    }
    
    updateConnectionStatus() {
        if (this.isConnected) {
            this.elements.connectionStatus.innerHTML = '<i class="fas fa-circle text-success me-1"></i>Conectado';
            this.elements.connectionStatus.className = 'badge bg-light text-dark me-2';
        } else {
            this.elements.connectionStatus.innerHTML = '<i class="fas fa-circle text-danger me-1"></i>Desconectado';
            this.elements.connectionStatus.className = 'badge bg-light text-dark me-2';
        }
    }
    
    updateExperimentStatus() {
        if (this.experimentRunning) {
            this.elements.experimentStatus.textContent = 'Executando';
            this.elements.experimentStatus.className = 'fw-bold status-running';
            this.elements.startBtn.disabled = true;
            this.elements.stopBtn.disabled = false;
        } else {
            this.elements.experimentStatus.textContent = 'Parado';
            this.elements.experimentStatus.className = 'fw-bold status-stopped';
            this.elements.startBtn.disabled = false;
            this.elements.stopBtn.disabled = true;
        }
    }
    
    updateCurrentData(data) {
        if (data.experience_code) {
            this.elements.experimentNumber.textContent = data.experience_code;
        }
        
        if (data.temperatura_atual) {
            const currentTemp = parseFloat(data.temperatura_atual);
            this.elements.currentTemp.textContent = currentTemp.toFixed(1) + '°C';
            
            // Animação baseada na mudança de temperatura
            if (this.lastTemperature !== null) {
                if (currentTemp > this.lastTemperature) {
                    this.elements.currentTemp.className = 'h4 fw-bold text-dark mb-0 temperature-rising';
                } else if (currentTemp < this.lastTemperature) {
                    this.elements.currentTemp.className = 'h4 fw-bold text-dark mb-0 temperature-falling';
                } else {
                    this.elements.currentTemp.className = 'h4 fw-bold text-dark mb-0';
                }
            }
            this.lastTemperature = currentTemp;
        }
        
        if (data.temperatura_desejada) {
            this.elements.targetTemp.textContent = parseFloat(data.temperatura_desejada).toFixed(1) + '°C';
        }
        
        if (data.tempo_ms) {
            const timeMs = parseInt(data.tempo_ms);
            const timeSeconds = (timeMs / 1000).toFixed(1);
            this.elements.timeMs.textContent = `${timeMs}ms (${timeSeconds}s)`;
        }
    }
    
    addDataToChart(data) {
        if (!data.tempo_ms || !data.temperatura_atual) return;
        
        const timeSeconds = (parseInt(data.tempo_ms) / 1000).toFixed(1);
        const currentTemp = parseFloat(data.temperatura_atual);
        const targetTemp = parseFloat(data.temperatura_desejada);
        
        // Adicionar novos dados
        this.chartData.labels.push(timeSeconds + 's');
        this.chartData.temperatures.push(currentTemp);
        this.chartData.targets.push(targetTemp);
        
        // Manter apenas os últimos 50 pontos para performance
        if (this.chartData.labels.length > 50) {
            this.chartData.labels.shift();
            this.chartData.temperatures.shift();
            this.chartData.targets.shift();
        }
        
        // Atualizar gráfico
        this.chart.update('none'); // Update sem animação para melhor performance
    }
    
    clearChart() {
        this.chartData.labels = [];
        this.chartData.temperatures = [];
        this.chartData.targets = [];
        this.chart.update();
    }
    
    async loadExperiments() {
        try {
            const response = await fetch('/api/experiments');
            const experiments = await response.json();
            
            if (experiments.length === 0) {
                this.elements.experimentsTable.innerHTML = `
                    <tr>
                        <td colspan="4" class="text-center text-muted">
                            <i class="fas fa-info-circle me-2"></i>
                            Nenhum experimento encontrado
                        </td>
                    </tr>
                `;
                return;
            }
            
            this.elements.experimentsTable.innerHTML = experiments.map(exp => `
                <tr onclick="window.open('Experiencias/${exp.filename}', '_blank')">
                    <td>
                        <i class="fas fa-file-csv text-success me-2"></i>
                        ${exp.filename}
                    </td>
                    <td>${exp.created}</td>
                    <td>${this.formatFileSize(exp.size)}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); window.open('Experiencias/${exp.filename}', '_blank')">
                            <i class="fas fa-download me-1"></i>Download
                        </button>
                    </td>
                </tr>
            `).join('');
            
        } catch (error) {
            console.error('Erro ao carregar experimentos:', error);
            this.elements.experimentsTable.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center text-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Erro ao carregar experimentos
                    </td>
                </tr>
            `;
        }
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    updateTime() {
        const now = new Date();
        this.elements.currentTime.textContent = now.toLocaleTimeString('pt-BR');
    }
    
    showAlert(title, message, type = 'info') {
        const modal = document.getElementById('alertModal');
        const modalTitle = document.getElementById('alertModalTitle');
        const modalBody = document.getElementById('alertModalBody');
        
        modalTitle.textContent = title;
        modalBody.innerHTML = `
            <div class="alert alert-${type} mb-0">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                ${message}
            </div>
        `;
        
        this.elements.alertModal.show();
        
        // Auto-fechar alerts de sucesso após 3 segundos
        if (type === 'success') {
            setTimeout(() => {
                this.elements.alertModal.hide();
            }, 3000);
        }
    }
}

// Inicializar aplicação quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    window.saunaApp = new SaunaCalango();
    
    // Adicionar indicador de carregamento global
    window.addEventListener('beforeunload', () => {
        document.body.style.opacity = '0.7';
    });
    
    console.log('🦎 Sauna de Calango - Interface carregada com sucesso!');
});