#!/usr/bin/env python3


"""
Este fichero se encarga de satisfacer el punto 4.b de la documentación a entregar:

"Debe incorporar todo el código necesario para su prueba, directamente ejecutable.
En este sentido, se recomienda incluir una sección principal para arrancar el servicio."
"""


from entornoiot import *


# Aquí tendrá lugar todo el código pedido
def main() -> None:
    """
    Se encarga de ejecutar todo el código de prueba e ir imprimiendo el proceso
    """
    sistema_iot = Sistema.obtener_instancia("temperatura", "127.0.0.1:9092")

    comprobador_delta = ComprobadorDelta(30 // 5 + 1, 10)
    comprobador_umbral = ComprobadorUmbral(25, comprobador_delta)
    calcula_estadisticos = CalculaEstadisticos(60 // 5, comprobador_umbral)

    calcula_estadisticos.nueva_calculadora("Media", CalculadoraMedia())
    calcula_estadisticos.nueva_calculadora("Moda", CalculadoraModa())
    calcula_estadisticos.nueva_calculadora("Máximo", CalculadoraMax())
    calcula_estadisticos.nueva_calculadora("Mínimo", CalculadoraMin())
    calcula_estadisticos.nueva_calculadora("Varianza", CalculadoraCuasiVar())
    calcula_estadisticos.nueva_calculadora("Mediana", CalculadoraMediana())

    sistema_iot.alta(calcula_estadisticos)

    sistema_iot.leer_sensor()


if __name__ == '__main__':
    main()
