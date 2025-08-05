# Sauna de Calango - Interface Web

## 🦎 Sobre o Projeto

Sistema de monitoramento em tempo real para experimentos de CTmax (Critical Thermal Maximum) em lagartos. Esta interface web moderna permite controlar experimentos, visualizar dados em tempo real e gerenciar histórico de experimentos.

## ✨ Funcionalidades

### 🎛️ Controle de Experimentos
- **Iniciar/Parar** experimentos via interface web
- **Status em tempo real** do experimento atual
- **Numeração automática** dos experimentos
- **Atalhos de teclado**: Ctrl+S (iniciar) / Ctrl+X (parar)

### 📊 Visualização de Dados
- **Gráfico em tempo real** das temperaturas (atual vs desejada)
- **Leituras atuais** com animações visuais
- **Indicadores de conexão** e status
- **Interface responsiva** para desktop e mobile

### 📁 Histórico de Experimentos
- **Lista completa** de experimentos realizados
- **Download direto** dos arquivos CSV
- **Informações detalhadas** (data, tamanho, etc.)
- **Atualização automática** da lista

## 🚀 Como Usar

### 1. Instalação das Dependências

```bash
# Instalar dependências Python
pipenv install

# Ou usando pip
pip install flask flask-socketio python-socketio pyserial
```

### 2. Executar a Aplicação

```bash
# Ativar ambiente virtual
pipenv shell

# Executar o servidor
python app.py
```

### 3. Acessar a Interface

Abra seu navegador e acesse: `http://localhost:5000`

## 🖥️ Interface Principal

### Painel de Controle
- **Botões de controle**: Iniciar/Parar experimentos
- **Status atual**: Estado do experimento e conexão
- **Leituras em tempo real**: Temperaturas e tempo

### Gráfico de Temperatura
- **Linha vermelha**: Temperatura atual do lagarto
- **Linha azul tracejada**: Temperatura desejada/programada
- **Atualização automática** a cada nova leitura
- **Zoom e interação** com os dados

### Histórico de Experimentos
- **Tabela interativa** com todos os experimentos
- **Colunas**: Nome do arquivo, data de criação, tamanho
- **Ações**: Download direto dos arquivos CSV

## 🔧 Estrutura Técnica

### Backend (Flask)
- **Rotas API REST** para controle de experimentos
- **WebSocket (SocketIO)** para dados em tempo real
- **Threading** para execução não-bloqueante
- **Gestão automática** de arquivos e numeração

### Frontend
- **HTML5 + Bootstrap 5** para interface responsiva
- **Chart.js** para gráficos interativos
- **Socket.IO Client** para comunicação em tempo real
- **CSS personalizado** com animações e efeitos

### Comunicação Serial
- **Detecção automática** da porta do Arduino
- **Leitura contínua** dos dados do sensor
- **Tratamento de erros** e reconexão automática

## 📡 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Interface principal |
| POST | `/api/start_experiment` | Iniciar experimento |
| POST | `/api/stop_experiment` | Parar experimento |
| GET | `/api/status` | Status atual |
| GET | `/api/experiments` | Lista de experimentos |

## 🔌 Eventos WebSocket

| Evento | Direção | Descrição |
|--------|---------|-----------|
| `connect` | Cliente → Servidor | Conexão estabelecida |
| `status` | Servidor → Cliente | Status inicial |
| `new_data` | Servidor → Cliente | Novos dados do sensor |
| `experiment_error` | Servidor → Cliente | Erro no experimento |

## 📁 Estrutura de Arquivos

```
sauna_de_calango/
├── app.py                 # Aplicação Flask principal
├── templates/
│   └── index.html         # Interface principal
├── static/
│   ├── css/
│   │   └── style.css      # Estilos personalizados
│   ├── js/
│   │   └── app.js         # JavaScript principal
│   └── images/            # Imagens e recursos
├── Experiencias/          # Arquivos CSV dos experimentos
├── ultima_exp.txt         # Contador de experimentos
└── Pipfile               # Dependências Python
```

## 🎨 Características Visuais

### Cores e Temas
- **Azul primário**: Cabeçalho e elementos principais
- **Verde**: Indicadores de sucesso e temperatura atual
- **Vermelho**: Alertas e temperatura em alta
- **Laranja**: Temperatura desejada
- **Cinza**: Elementos secundários

### Animações
- **Pulsação**: Para mudanças de temperatura
- **Transições suaves**: Em botões e cards
- **Loading spinners**: Durante operações
- **Hover effects**: Para melhor interatividade

## 🛠️ Desenvolvimento

### Modificações Possíveis
1. **Adicionar filtros** no histórico de experimentos
2. **Exportar gráficos** como imagens
3. **Configurações avançadas** do experimento
4. **Notificações push** para eventos importantes
5. **Dashboard** com estatísticas gerais

### Extensões Sugeridas
- **Banco de dados** para armazenamento persistente
- **Autenticação** para múltiplos usuários
- **API REST completa** para integração externa
- **Aplicativo mobile** complementar

## 🐛 Resolução de Problemas

### Arduino Não Detectado
1. Verificar conexão USB
2. Instalar drivers CH340 se necessário
3. Verificar porta serial no código

### Interface Não Carrega
1. Verificar se o Flask está rodando
2. Verificar se a porta 5000 está livre
3. Verificar console do navegador para erros

### Dados Não Aparecem
1. Verificar conexão WebSocket
2. Verificar formato dos dados do Arduino
3. Verificar console para erros de parsing

## 📊 Exemplo de Dados

Formato esperado do Arduino (separado por `;`):
```
1000;25.5;30.0
2000;26.1;30.0
3000;27.8;30.0
```

- **Campo 1**: Tempo em milissegundos
- **Campo 2**: Temperatura atual em °C
- **Campo 3**: Temperatura desejada em °C

## 🤝 Contribuições

Este projeto é parte de uma pesquisa científica. Sugestões e melhorias são bem-vindas através de:
- Issues no repositório
- Pull requests com novas funcionalidades
- Feedback sobre usabilidade
- Relatórios de bugs

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e de pesquisa científica.

---

**Desenvolvido com ❤️ para a comunidade científica** 🦎🔬