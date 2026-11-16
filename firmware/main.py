from machine import Pin, PWM, SPI
import time
from red import conectar
from cliente_mqtt import ClienteMQTT
import teclado
from teclado import leer_teclado
import mfrc522
import sys
import select

# 1. Configuración del Servomotor (Pin 13) - Simula el cerrojo
servo = PWM(Pin(13), freq=50)

def mover_servo(angulo):
    duty = int(1638 + (angulo / 180) * (7864 - 1638))
    servo.duty_u16(duty)

# Posición inicial: Cerrado (0 grados)
mover_servo(0)
puerta_abierta = False

# 2. Configuración de Red y MQTT
topic_Propio = "prueba/103_servo"
topic_suscribir = "Prueba/suscribir_servo"

conectar("Wokwi-GUEST", "")

mqtt = ClienteMQTT("Grupo105_Servo", "broker.emqx.io")
mqtt.conectar()
mqtt.publicar(topic_Propio, "Cerradura inteligente conectada y lista")

# Callback inteligente para recibir "ABRIR" o "CERRAR" por MQTT
def controlar_servo(topico, mensaje):
    global puerta_abierta
    print("Comando recibido por MQTT:")
    comando = mensaje.decode().strip().upper() # Convertir a mayúsculas para evitar errores
    print(comando)
    
    if comando == "ABRIR":
        mover_servo(90) # Ángulo de apertura de la cerradura
        puerta_abierta = True
        print("--> ¡Cerradura ABIERTA desde el celular!")
        mqtt.publicar(topic_Propio, "Estado: Cerradura ABIIERTA")
    elif comando == "CERRAR":
        mover_servo(0)  # Ángulo de cierre
        puerta_abierta = False
        print("--> ¡Cerradura CERRADA desde el celular!")
        mqtt.publicar(topic_Propio, "Estado: Cerradura CERRADA")
    else:
        print("Comando no reconocido. Use 'ABRIR' o 'CERRAR'.")

mqtt.suscribirse(topic_suscribir, controlar_servo)

# Consola serial local
serial = select.poll()
serial.register(sys.stdin, select.POLLIN)

# 3. Configuración del Bus SPI y Lector RFID
spi = SPI(2, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(23), miso=Pin(19))

rdr = mfrc522.MFRC522(spi, cs_pin=5, rst_pin=22)
rdr.init() 

# Variables de control de acceso
clave_maestra = "1410"
intentos_actual = ""
intentos_fallidos = 0
TARJETA_AUTORIZADA = "0103040000" 

print("==========================================")
print(" Cerradura Inteligente: Teclado + RFID + MQTT")
print("==========================================")

# 4. Bucle Principal No Bloqueante
while True:
    
    # --- A. GESTIÓN DEL TECLADO MATRICIAL ---
    tecla = leer_teclado()
    if tecla is not None and tecla.strip() != "":
        intentos_actual += tecla
        print(f"Tecla presionada: {tecla}")
        
        if len(intentos_actual) == 4:
            if intentos_fallidos >= 3:
                print("Sistema Bloqueado: Use la app del celular para desbloquear.")
            else:
                if intentos_actual == clave_maestra:
                    print("¡Acceso concedido por Teclado! Abriendo...")
                    intentos_fallidos = 0
                    mover_servo(90) # Abre
                    mqtt.publicar(topic_Propio, "Acceso concedido por Teclado (Abierto)")
                    time.sleep(3)   # Tiempo abierta
                    mover_servo(0)  # Cierra automáticamente
                    print("Cerradura cerrada automáticamente.")
                else:
                    intentos_fallidos += 1
                    intentos_restantes = 3 - intentos_fallidos
                    print(f"Clave incorrecta. Intentos restantes: {intentos_restantes}")
                    if intentos_fallidos == 3:
                        print("¡Bloqueado por seguridad!")
            
            intentos_actual = ""

    # --- B. GESTIÓN DEL LECTOR RFID ---
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK and len(raw_uid) > 0:
            uid_str = "".join("%02x" % x for x in raw_uid)
            print(f"¡Tarjeta RFID detectada! UID: {uid_str}")
            
            if uid_str == TARJETA_AUTORIZADA:
                print("¡Acceso concedido por Tarjeta RFID! Abriendo...")
                intentos_fallidos = 0 # Resetea bloqueos de teclado al usar llave física válida
                mover_servo(90) # Abre
                mqtt.publicar(topic_Propio, "Acceso concedido por RFID (Abierto)")
                time.sleep(3)
                mover_servo(0)  # Cierra
                print("Cerradura cerrada automáticamente.")
            else:
                print("Tarjeta RFID no autorizada.")
                
            time.sleep(1)

    # --- C. REVISAR MQTT Y CONSOLA SERIAL ---
    mqtt.revizarmensaje()
    
    if serial.poll(0):
        mensaje = sys.stdin.readline().strip().upper()
        if mensaje == "ABRIR":
            mover_servo(90)
            print("Cerradura abierta desde consola local.")
        elif mensaje == "CERRAR":
            mover_servo(0)
            print("Cerradura cerrada desde consola local.")

    time.sleep_ms(20)