import network
import time
import urequests
from machine import Pin
import dht

# Função para conectar ao Wi-Fi
def conectar_wifi(ssid, senha):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, senha)
    while not wlan.isconnected():
        time.sleep(1)
    print('Conectado ao Wi-Fi:', wlan.ifconfig())
    return wlan


INTERVALO_ENVIO = 20 

# Inicialização de dispositivos
sensor_dht = dht.DHT11(Pin(5))
rele = Pin(3, Pin.OUT)

# Conectar ao Wi-Fi
conectar_wifi("ALICE", "1repolho")
# Função para ler os dados do sensor
def ler_sensor(sensor):
    sensor.measure()
    temp = sensor.temperature()
    umid = sensor.humidity()
    print(f'Temperatura está: {temp} °C')
    print(f'Umidade está: {umid} %')
    return temp, umid

# Função para controlar o relé
def controlar_rele(temp, umid, limite_temp=31, limite_umid=70):
    if temp > limite_temp or umid > limite_umid:
        rele.on()
        print('Ligando o relé...')
    else:
        rele.off()
        print('Desligando o relé')

# Função para enviar os dados ao ThingSpeak
def enviar_para_thingspeak(temp, umid, api_key):
    dados = {
        'api_key': "4FTP3G1P858VRHIC",
        'field1': temp,
        'field2': umid
    }
    try:
        resposta = urequests.post("https://api.thingspeak.com/update", json=dados)
        resposta.close()
        print('Dados enviados com sucesso.')
    except Exception as e:
        print('Erro ao enviar dados:', e)

# Loop principal
while True:
    try:
        temperatura, umidade = ler_sensor(sensor_dht)
        controlar_rele(temperatura, umidade)
        enviar_para_thingspeak(temperatura, umidade, "4FTP3G1P858VRHIC")
    except Exception as erro:
        print('Erro no loop principal:', erro)
    
    time.sleep(INTERVALO_ENVIO)

    



