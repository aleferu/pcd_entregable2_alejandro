# Implementación en Python

Se utiliza la utilidad de los paquetes en Python. El paquete se llama `entornoiot`, y toda la implementación se encuentra en ese directorio.

El fichero `sensor.py` se encarga de realizar la simulación del sensor de temperaturas. Está pensado para ser ejecutado de una manera similar a la siguiente

```sh
nohup python -m sensor localhost:9092 temperatura &
```

## Requisitos

La funcionalidad de esta entrega supone que se está ejecutando en un sistema donde kafka esté instalado y ejecutándose. Para instalar la librería de python se puede ejecutar el comando:

```sh
pip install kafka-python
```

Si existe algún problema se recomienda probar con `kafka-python-ng`, pues parece ser que es más compatible con versiones nuevas de Python.

## Sensor de temperatura

Para simular el comportamiento de un sensor de temperatura que actúa cada cinco segundos se ha creado un script llamado `sensor.py`. Este script, cada cinco segundos (aunque se puede cambiar) envía al servidor de Kafka que se indique y al tópico que se indique un JSON que contiene un *timestamp* y un número obtenido de una distribución normal de media 20 y desviación típica 4, siendo este último valor la simulación de la temperatura (obviamente varía demasiado para ser real pero la idea es que varíe mucho para poder observar cambios en los diferentes cálculos que se realizan).

## Código de prueba

Se deja a disposición, tal y como pide el enunciado, un script a modo de demostración del código escrito en uso. El fichero de prueba se llama `codigo_prueba.py` y está pensado para ser ejecutado.

Este fichero de prueba supone que hay una instancia de kafka ejecutándose en el sistema y que el script que simula el sensor de temperaturas `sensor.py` está ejecutándose.

En este script se muestra que lo que se pide en el enunciado de la entrega es posible hacerlo con la implementación realizada.

## Tests

Los ficheros de tests son `test_*.py`, donde en la estrella se encuentra la clase de la cual se está comprobando el correcto funcionamiento.

Para comprobarlo todo se ha utilizado la herramienta [pytest](https://docs.pytest.org/en/stable/ 'pytest website'). Una vez instalada se puede ejecutar el comando `pytest` en el mismo directorio en el que se encuentra este README (si no funciona se puede utilizar la utilidad de ejecutar módulos en python `python -m pytest`). Si se ejecuta desde otro directorio se puede añadir la ruta al directorio como argumento del comando. Si se quiere más información se puede utilizar la flag `-v` para obtener más información.

Se facilita un script para ejecutar los tests, fichero `ejecutar-tests.sh`.
