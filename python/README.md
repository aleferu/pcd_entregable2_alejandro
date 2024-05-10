# Implementación en Python

**TODO**

## Requisitos

La funcionalidad de esta entrega supone que se está ejecutando en un sistema donde kafka esté instalado y ejecutándose. Para instalar la librería de python se puede ejecutar el comando:

```sh
pip install kafka-python
```

## Sensor de temperatura

Para simular el comportamiento de un sensor de temperatura que actúa cada cinco segundos se ha creado un script llamado `sensor.py`. Este script... **TODO**

## Código de prueba

Se deja a disposición, tal y como pide el enunciado, un script a modo de demostración del código escrito en uso. El fichero de prueba se llama `codigo_prueba.py` y está pensado para ser ejecutado.

Este fichero de prueba supone que hay una instancia de kafka ejecutándose en el sistema y que el script que simula el sensor de temperaturas `sensor.py` está ejecutándose.

## Tests

Los ficheros de tests son `test_*.py`, donde en la estrella se encuentra la clase de la cual se está comprobando el correcto funcionamiento.

Para comprobarlo todo se ha utilizado la herramienta [pytest](https://docs.pytest.org/en/stable/ 'pytest website'). Una vez instalada se puede ejecutar el comando `pytest` en el mismo directorio en el que se encuentra este README (si no funciona se puede utilizar la utilidad de ejecutar módulos en python `python -m pytest`). Si se ejecuta desde otro directorio se puede añadir la ruta al directorio como argumento del comando. Si se quiere más información se puede utilizar la flag `-v` para obtener más información.

Se facilita un script para ejecutar los tests, fichero `ejecutar-tests.sh`.

## TODO

- Kafka cosas. Productor y consumer.
