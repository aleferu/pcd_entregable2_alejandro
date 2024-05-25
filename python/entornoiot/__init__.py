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
from typing import Optional

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
    - _topic: str que representa el tópico Kafka en el que llegan los datos
    - _server_address: str que representa la dirección donde el servidor Kafka está alojado
    - _sensor: instancia de KafkaConsumer que lee los datos que se produzcan sobre el tópico '_topic'
    - _subscriptores: instancias de ManejaTemperaturas a las que enviar la temperatura cuando se reciban.
    """
    _instancia: Optional["Sistema"] = None
    "Única instancia que debería existir de la clase"

    _topic: str
    "str que representa el tópico Kafka en el que llegan los datos"

    _server_address: str
    "str que representa la dirección donde el servidor Kafka está alojado"

    _sensor: KafkaConsumer
    "Instancia de KafkaConsumer que lee los datos que se produzcan sobre el tópico '_topic'"

    _subscriptores: list[ManejaTemperaturas]
    "Instancias de ManejaTemperaturas a las que enviar la temperatura cuando se reciban."

    def __init__(self, topic: str, server_address: str):
        """
        Crea una instancia de Sistema. Sin embargo, esta clase sigue el patrón de diseño Singleton
        y nunca debería instanciarse usando su constructor.

        Parámetros
        ----------
        - topic: str que representa el tópico Kafka en el que llegan los datos
        - server_adress: str que representa la dirección donde el servidor Kafka está alojado

        Lanza
        -----
        - kafka.errors.NoBrokersAvailable si el servidor de Kafka no se encuentra
        """
        self._topic = topic
        self._server_address = server_address
        self._sensor = KafkaConsumer(
            self._topic,
            bootstrap_servers=self._server_address,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self._subscriptores = list()

    @classmethod
    def obtener_instancia(cls, topic: Optional[str] = None, server_address: Optional[str] = None) -> "Sistema":
        """
        Método de clase encargado de instancia el único objeto que debería existir de la clase y de distribuir
        dicho objeto donde se necesite.

        Los parámetros se usarán solo en el caso de que se necesite crear el objeto y son opcionales.

        Parámetros
        ----------
        - topic: str que representa el tópico Kafka en el que llegan los datos
        - server_adress: str que representa la dirección donde el servidor Kafka está alojado

        Lanza
        -----
        - kafka.errors.NoBrokersAvailable si el servidor de Kafka no se encuentra
        - ValueError si el objeto no ha sido creado y no se han proporcionado alguno de los argumentos
        """
        if not cls._instancia:
            if not topic or not server_address:
                raise ValueError("No existe una instancia de Sistema ya creada y no se han especificado parámetros")
            cls._instancia = Sistema(topic, server_address)
        return cls._instancia

    def alta(self, nuevo_subscriptor: ManejaTemperaturas):
        """
        Método encargado de añadir a la lista de subscriptores un nuevo objeto.

        Parámetros
        ----------
        - nuevo_subscriptor: Instancia de ManejaTemperaturas a añadir a la lista

        Lanza
        -----
        - ValueError si el objeto ya va a ser notificado, sea a través de una cadena o porque se encuentre en la lista
        """
        for subscriptor in self._subscriptores:
            if nuevo_subscriptor is subscriptor:
                raise ValueError("El objeto ya es suscriptor.")
            while miembro_cadena := subscriptor.manejador_temperaturas:
                if nuevo_subscriptor is miembro_cadena:
                    raise ValueError("El objeto ya va a ser notificado a través de una cadena.")
        self._subscriptores.append(nuevo_subscriptor)

    def baja(self, subscriptor: ManejaTemperaturas):
        """
        Método encargado de eliminar un objeto de la lista de subscriptores.

        Parámetros
        ----------
        - subscriptor: Instancia de ManejaTemperaturas a eliminar a la lista

        Lanza
        -----
        - ValueError si el objeto ya no se encuentra en la lista
        """
        try:
            self._subscriptores.remove(subscriptor)
        except ValueError:
            raise ValueError("El objeto no iba a ser notificado de primeras.")

    def leer_sensor(self):
        """
        Método encargado de recibir las temperaturas y los tiempos, imprimir la información, y enviar la temperatura
        a los objetos que se hayan suscrito.

        AVISO: bucle infinito
        """
        for lectura in self._sensor:
            mensaje = lectura.value
            timestamp = mensaje["timestamp"]
            temperatura = float(mensaje["temperatura"])
            print(f"{timestamp}: {round(temperatura, 3)}")
            self.notificar(temperatura)
            print()

    def notificar(self, temperatura: float):
        """
        Método encargado de enviar la temperatura a los objetos que se hayan suscrito.
        """
        for subscriptor in self._subscriptores:
            subscriptor.nueva_temperatura(temperatura)
