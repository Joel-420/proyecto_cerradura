Sistema de Control de Acceso Inteligente con ESP32
Proyecto de cerradura inteligente multi-modal desarrollado en MicroPython utilizando un microcontrolador ESP32. El sistema integra múltiples métodos de autenticación local (teclado matricial y tarjetas RFID) junto con conectividad IoT vía MQTT para supervisión y control remoto.
Componentes Utilizados
 * Microcontrolador: ESP32 NodeMCU.
 * Lector RFID: MFRC522 (Interfaz SPI).
 * Teclado Matricial: 4x4 (Para autenticación por PIN).
 * Actuador: Servomotor (simulando el mecanismo de bloqueo/cerrojo del pestillo).
 * Conectividad: Módulo Wi-Fi interno del ESP32 y broker MQTT público (broker.emqx.io).
Funcionalidades Implementadas
 * Autenticación Local por PIN:
   * Ingreso de contraseña de 4 dígitos mediante el teclado matricial.
   * Sistema de seguridad con bloqueo temporal tras 3 intentos fallidos consecutivos.
 * Autenticación por Tarjeta/Llavero RFID:
   * Lectura de UID único mediante protocolo SPI.
   * Validación contra tarjeta maestra autorizada con reseteo automático de los intentos fallidos del teclado.
 * Control y Alertas por MQTT (IoT):
   * Control Remoto: Capacidad de abrir y cerrar la cerradura enviando comandos de texto (ABRIR / CERRAR) desde una aplicación móvil o cliente MQTT.
   * Monitoreo en Tiempo Real: Publicación automática de eventos en el broker (accesos concedidos, intentos fallidos de PIN, alertas de tarjetas no autorizadas y estados de la cerradura).
   * Protección Anti-Retain: Mecanismo de gracia al arranque para ignorar mensajes fantasma retenidos por el broker al reiniciar el dispositivo.
 * Arquitectura No Bloqueante:
   * Bucle principal optimizado para escuchar de forma simultánea el teclado, el sensor RFID y los mensajes de red sin que un periférico congele a los demás.
Estructura del Proyecto
 * main.py: Bucle principal de ejecución, gestión de eventos, lógica de control de acceso y cliente MQTT.
 * teclado.py: Manejo del escaneo de teclas del teclado matricial.
 * mfrc522.py: Librería de control para la comunicación SPI con el lector RFID.
 * red.py: Configuración y conexión a la red Wi-Fi.
 * cliente_mqtt.py: Clase auxiliar para la conexión, suscripción y publicación de mensajes MQTT.
