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


from kafka import KafkaConsumer
import json

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

del estadisticos, cadena

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
    _instancia: "Sistema"
    _topic: str
    _server_address: str
    _sensor: KafkaConsumer
    _subscriptores: list[ManejaTemperaturas]

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
