from machine import Pin
import time
# Definir los pines para las Filas (Outputs) y Columnas (Inputs con Pull-up interno)
fila_pines = [12, 14, 27, 32]
columna_pines = [25, 26, 33, 2]

# Mapa de caracteres del teclado matricial 4x4
teclas = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Inicializar filas como salidas
filas = [Pin(pin, Pin.OUT) for pin in fila_pines]
# Inicializar columnas como entradas con resistencia pull-up interna
columnas = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in columna_pines]

def leer_teclado():
    for f_idx, fila in enumerate(filas):
        # Poner la fila actual en nivel bajo (0V)
        fila.value(0)
        
        for c_idx, columna in enumerate(columnas):
            # Si la columna lee 0, significa que se presionó el botón de esa intersección
            if columna.value() == 0:
                # Esperar a que se suelte la tecla para evitar rebotes múltiples
                while columna.value() == 0:
                    time.sleep_ms(50)
                fila.value(1) # Restaurar fila
                return teclas[f_idx][c_idx]
                
        # # Restaurar la fila a nivel alto (1V) antes de pasar a la siguiente
        fila.value(1)

def validacion(clave,intentos_fallidos):
    intento_actual = ""
    acceso = False
    if intentos_fallidos == 3:
        print("Bloqueado solo se puede abrir desde el celular")
        acceso = False
    if intentos_fallidos < 3:
        while len(intento_actual) < 4:
            tecla = leer_teclado()
            if tecla is not None and tecla.strip() != "":
                intento_actual += tecla
                print(f"¡Tecla presionada!: {tecla}")
        if clave == intento_actual:
            intentos_fallidos = 0
            acceso = True
            print("Bienvenido")
        else: 
            intentos_fallidos += 1
            acceso = False
            intentos_rest = 3 - intentos_fallidos
            print(f"Acceso denegad, intentos restantes: {intentos_rest}")
    return acceso, intentos_fallidos