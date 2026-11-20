from datetime import datetime


class ControladorCerradura:
    def __init__(self, max_intentos=3, pin_inicial="1234"):
        self.puerta_abierta = False
        self.intentos_fallidos = 0
        self.max_intentos = max_intentos
        self.bloqueado = False
        self.pin_actual = pin_inicial
        self.ultimo_metodo = "SISTEMA"
        self.registros = [
            ["08:00:00", "SISTEMA", "Panel de control inicializado", "AUTORIZADO"]
        ]

    def _crear_registro(self, metodo, detalle, estado):
        hora = datetime.now().strftime("%H:%M:%S")
        nuevo = [hora, metodo, detalle, estado]
        self.registros.insert(0, nuevo)
        return nuevo

    def abrir_puerta(self, metodo="MQTT / PANEL"):
        if self.bloqueado:
            return False, self._crear_registro(metodo, "Apertura denegada: sistema bloqueado", "DENEGADO")
        self.puerta_abierta = True
        self.ultimo_metodo = metodo
        return True, self._crear_registro(metodo, "Puerta ABIERTA correctamente", "AUTORIZADO")

    def cerrar_puerta(self, metodo="MQTT / PANEL"):
        self.puerta_abierta = False
        self.ultimo_metodo = metodo
        return True, self._crear_registro(metodo, "Puerta CERRADA correctamente", "AUTORIZADO")

    def simular_rfid_valido(self, uid="A4F2"):
        if self.bloqueado:
            return False, self._crear_registro("RFID", "Lectura ignorada por bloqueo activo", "DENEGADO")
        self.intentos_fallidos = 0
        self.puerta_abierta = True
        self.ultimo_metodo = "RFID"
        return True, self._crear_registro("RFID", f"Tarjeta autorizada (UID: {uid})", "AUTORIZADO")

    def registrar_intento_fallido(self, activar_alarma=True):
        if self.bloqueado:
            return self._crear_registro("TECLADO", "Teclado bloqueado por seguridad", "DENEGADO")

        self.intentos_fallidos += 1
        if self.intentos_fallidos >= self.max_intentos and activar_alarma:
            self.bloqueado = True
            self.puerta_abierta = False
            self.ultimo_metodo = "BLOQUEADO"
            return self._crear_registro("ALARMA", f"{self.max_intentos} intentos fallidos: sistema bloqueado", "DENEGADO")

        return self._crear_registro("TECLADO", f"PIN incorrecto ({self.intentos_fallidos}/{self.max_intentos})", "DENEGADO")

    def resetear_alarma(self):
        self.bloqueado = False
        self.intentos_fallidos = 0
        return self._crear_registro("SISTEMA", "Alarma restablecida por administrador", "AUTORIZADO")

    def cambiar_pin(self, nuevo_pin):
        nuevo_pin = nuevo_pin.strip()
        if len(nuevo_pin) != 4 or not nuevo_pin.isdigit():
            return False, "Ingrese 4 dígitos numéricos", self._crear_registro("SEGURIDAD", "Intento de cambio de PIN inválido", "DENEGADO")

        self.pin_actual = nuevo_pin
        return True, "", self._crear_registro("SEGURIDAD", "Nuevo PIN maestro sincronizado", "AUTORIZADO")