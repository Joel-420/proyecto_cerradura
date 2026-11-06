from umqtt.simple import MQTTClient

class ClienteMQTT:
    def __init__(self, id_cliente, broker):
        self._cliente = MQTTClient(id_cliente, broker)
    
    def conectar(self):
        self._cliente.connect()

    def publicar(self, topico, mensaje):
        self._cliente.publish(topico.encode(), mensaje.encode())
        print("MENSAJE ENVIADO")
        print(mensaje)

    def suscribirse(self,topic, funcion):
        self._cliente.set_callback(funcion)
        self._cliente.subscribe(topic.encode())
        print("Me suscribi")
    
    def revizarmensaje(self):
        self._cliente.check_msg()

    