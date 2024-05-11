#!/usr/bin/env python3


import kafka
import time
import sys
import json
import random
from datetime import datetime


class SensorTemperatura:
    """
    Clase encargada de simular el comportamiento de un sensor de temperaturas.
    El sensor se supone que debe de leer la temperatura actual y debe enviarla
    a un entorno IoT usando Kafka.

    Atributos
    ---------
    - topic: string que representa el tópico de Kafka en el que se envían las lecturas
    - frecuencia: número que representa cada cuánto el sensor lee la temperatura
    - producer: instancia de KafkaProducer que se encarga del envío de información
    """
    topic: str
    "String que representa el tópico de kafka en el que se envían las lecturas"

    frecuencia: float
    "Número que representa cada cuánto el sensor lee la temperatura"

    producer: kafka.KafkaProducer
    "Instancia de KafkaProducer que se encarga del envío de información"

    def __init__(self, server_address: str, topic: str, frecuencia: str):
        """
        Crea una instancia del sensor de temperaturas.

        Parámetros
        ----------
        - server_address: string que representa la dirección donde está alojado Kafka
        - topic: string que representa el tópico de kafka en el que se envían las lecturas
        - frecuencia: string que coniene un número de segundos a esperar entre lectura y lectura
        """
        self.topic = topic
        self.frecuencia = float(frecuencia)
        self.producer = kafka.KafkaProducer(
            bootstrap_servers=server_address,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def empezar_escritura(self):
        """
        Empieza las lecturas de temperatura. Las lecturas se han simulado utilizando una
        distribución normal de media 20 y desviación típica 4. La fecha asociada a la
        temperaturas será la de ese momento. El envío se realiza en forma de JSON.

        AVISO: Bucle infinito.
        """
        while True:
            temperatura = random.normalvariate(20, 4)
            mensaje = {
                "timestamp": str(datetime.now()),
                "temperatura": temperatura
            }
            self.producer.send(self.topic, value=mensaje)
            time.sleep(self.frecuencia)


if __name__ == '__main__':
    producer = SensorTemperatura(sys.argv[1], sys.argv[2], "5")
    producer.empezar_escritura()
