"""
EntornoIOT
==========

Se proporcionan las clases que he visto necesario hacer para cumplir
con lo especificado en el enunciado de la entrega.

La idea es utilizar las instancias de las demás clases a través de Sistema.

Asignatura: Fundamentos de Programación para Ciencia de Datos
Segunda práctica entregable: Sistema de Gestión de Datos de Sensores en un Entorno IoT
Alumno: Alejandro Fernández Sánchez

Las clases proporcionadas son:
- CalculadoraEstadistico
- CalculadoraMedia
- CalculadoraModa
- CalculadoraMax
- CalculadoraMin
- CalculadoraCuasiVar
- CalculadoraMediana
- ManejaTemperaturas,
- CalculaEstadisticos,
- ComprobadorUmbral,
- ComprobadorDelta
- Sistema
"""


# Se necesitan las siguientes librerías externas
from kafka import KafkaConsumer
import json

# Clases a importar
from .estadisticos import (
    CalculadoraEstadistico,
    CalculadoraMedia,
    CalculadoraModa,
    CalculadoraMax,
    CalculadoraMin,
    CalculadoraCuasiVar,
    CalculadoraMediana
)
from .cadena import (
    ManejaTemperaturas,
    CalculaEstadisticos,
    ComprobadorUmbral,
    ComprobadorDelta
)

# Para no poder acceder a los submódulos en un
# from entornoiot import *
del estadisticos, cadena

# Se indica qué clases se importan cuando se hace un 'from entornoiot import *'
__all__ = [
    "CalculadoraEstadistico",
    "CalculadoraMedia",
    "CalculadoraModa",
    "CalculadoraMax",
    "CalculadoraMin",
    "CalculadoraCuasiVar",
    "CalculadoraMediana",
    "ManejaTemperaturas",
    "CalculaEstadisticos",
    "ComprobadorUmbral",
    "ComprobadorDelta",
    "Sistema"
]


class Sistema:
    """
    Clase que se encarga de recibir la temperatura y enviarla a los objetos interesados.

    Se trata de un singleton, así que su constructor no debería ser llamadado nunca.

    Para la instanciación se deja a disposición un método llamada 'obtener_instancia'.

    Atributos
    ---------
    - _instancia: única instancia que debería existir de la clase
    - _topic: string que representa el tópico Kafka en el que llegan los datos
    - _server_address: string que representa la dirección donde el servidor Kafka está alojado
    - _sensor: instancia de KafkaConsumer que lee los datos que se produzcan sobre el tópico '_topic'
    - _subscriptores: instancias de ManejaTemperaturas a las que enviar la temperatura cuando se reciban.
    """
    _instancia: "Sistema"
    "Única instancia que debería existir de la clase"

    _topic: str
    "String que representa el tópico Kafka en el que llegan los datos"

    _server_address: str
    "String que representa la dirección donde el servidor Kafka está alojado"

    _sensor: KafkaConsumer
    "Instancia de KafkaConsumer que lee los datos que se produzcan sobre el tópico '_topic'"

    _subscriptores: list[ManejaTemperaturas]
    "Instancias de ManejaTemperaturas a las que enviar la temperatura cuando se reciban."

    def __init__(self, topic: str, server_address: str):
        self._topic = topic
        self._server_address = server_address
        self._sensor = KafkaConsumer(
            self._topic,
            bootstrap_servers=self._server_address,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self._subscriptores = list()

    def obtener_instancia(self) -> "Sistema":
        if not self._instancia:
            self._instancia = Sistema(self._topic, self._server_address)
        return self._instancia

    def alta(self, nuevo_subscriptor: ManejaTemperaturas):
        for subscriptor in self._subscriptores:
            if nuevo_subscriptor is subscriptor:
                raise ValueError("El objeto ya es suscriptor.")
            while miembro_cadena := subscriptor.manejador_temperaturas:
                if nuevo_subscriptor is miembro_cadena:
                    raise ValueError("El objeto ya va a ser notificado a través de una cadena.")
        self._subscriptores.append(nuevo_subscriptor)

    def baja(self, subscriptor: ManejaTemperaturas):
        try:
            self._subscriptores.remove(subscriptor)
        except ValueError:
            raise ValueError("El objeto no iba a ser notificado de primeras.")

    def leer_sensor(self):
        for lectura in self._sensor:
            mensaje = lectura.value
            timestamp = mensaje["timestamp"]
            temperatura = float(mensaje["temperatura"])
            print(f"{timestamp}: {round(temperatura, 3)}")
            self.notificar(temperatura)
            print()

    def notificar(self, temperatura: float):
        for subscriptor in self._subscriptores:
            subscriptor.manejar_temperatura(temperatura)
