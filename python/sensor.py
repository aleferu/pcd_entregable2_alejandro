#!/usr/bin/env python3


import kafka
import time
import sys
import json
import random
from datetime import datetime


class SensorTemperatura:
    topic: str
    frecuencia: float
    producer: kafka.KafkaProducer

    def __init__(self, server_address: str, topic: str, frecuencia: str):
        self.topic = topic
        self.frecuencia = float(frecuencia)
        self.producer = kafka.KafkaProducer(
            bootstrap_servers=server_address,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def empezar_escritura(self):
        while True:
            timestamp = datetime.now()
            temperatura = random.normalvariate(20, 4)
            mensaje = {
                "timestamp": str(datetime.now()),
                "temperatura": temperatura
            }
            self.producer.send(self.topic, value=mensaje)
            time.sleep(self.frecuencia)


if __name__ == '__main__':
    producer = SensorTemperatura(sys.argv[1], sys.argv[2], sys.argv[3])
    producer.empezar_escritura()
