// Software de controle de temperatura funcionando no modo aquecimento
// Desenvolvido por Me. Raphael de Jesus Lisboa Aquino
// 2022
// Objetivo: melhorar a repetibilidade de experimentos biológicos de
// medidas de CTmáx.
// Sobre o hardware:
// Pino digital de leitura da temperatura: 3
// Pinos de controle de potência:
// digital 7 para controle da temperatura do VIDRO
// digital 8 para controle da temperatura do AR
// Dois termômetros one-Wire para função: Temperatura ar e Temperatura vidro no pino 3

#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 3 // Linha de dados vai para o pino digital 3
#define PinoReleVidro 7

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DeviceAddress outsideThermometer;

float pot = 0; // potenciômetro
float tempAtual; // temperatura do sensor
float aquecimento = 24; //controle da temperatura
float tempAlvo;   // temperatura desejada
unsigned long previousMillis = 0;
unsigned long previousMin = 0;
const long interval = 1000; // intervalo de 1 segundo
const long minuto = 60000; // intervalo de 1 minuto

void setup() {
  Serial.begin(9600);

  pinMode(PinoReleVidro, OUTPUT); //configuração do pino
  
  sensors.begin();
  
  if (!sensors.getAddress(outsideThermometer, 0)) {
    Serial.println("Unable to find address for Device 0");
  }
}

void loop() {
  unsigned long currentMillis = millis();
  if ((currentMillis - previousMillis) >= interval) {
    previousMillis = currentMillis;
    sensors.requestTemperatures();
    tempAtual = sensors.getTempC(outsideThermometer);
    pot = analogRead(A1);
    tempAlvo = map(pot, 0, 1023, 23, 70);

    Serial.print(tempAtual);
    Serial.print(";");
    Serial.print(currentMillis);
    Serial.print(";");
    Serial.println(tempAlvo);
  }

  if ((currentMillis - previousMin) >= minuto && aquecimento <= tempAlvo) { //verifica se ja passou 1 minuto e se ja atingiu a tmperatura alvo
    // Incrementa a temperatura alvo em 1 grau
    aquecimento = aquecimento + 1;
    // Atualiza o tempo do minuto
    previousMin = currentMillis;
  }

  if (tempAtual > aquecimento) {
    digitalWrite(PinoReleVidro, HIGH);
  }
  else if (tempAtual <= aquecimento) {
    digitalWrite(PinoReleVidro, LOW);
  }
}
