from abc import ABC
from .estadisticos import CalculadoraEstadistico
from typing import Optional


class ManejaTemperaturas(ABC):
    _temperaturas: list[float]
    _indice_actual: int
    _temperaturas_a_mantener: int
    _is_lista_entera: bool
    _manejador_temperaturas: Optional["ManejaTemperaturas"]

    def __init__(self, temperaturas_a_mantener: int, manejador_temperaturas: Optional["ManejaTemperaturas"] = None):
        self._temperaturas = list()
        self._indice_actual = 0
        self._temperaturas_a_mantener = temperaturas_a_mantener
        self._is_lista_entera = self._indice_actual == self._temperaturas_a_mantener
        self._manejador_temperaturas = manejador_temperaturas

    def manejar_temperatura(self, nueva_temperatura: float):
        if not self._is_lista_entera:
            self._temperaturas.append(nueva_temperatura)
        else:
            self._temperaturas[self._indice_actual] = nueva_temperatura
        self._indice_actual = (self._indice_actual + 1) % self._temperaturas_a_mantener
        if self._indice_actual == 0 and not self._is_lista_entera:
            self._is_lista_entera = True


class CalculaEstadisticos(ManejaTemperaturas):
    _calculadoras_de_estadisticos: dict[str, CalculadoraEstadistico]

    def __init__(self, temperaturas_a_mantener: int, manejador_temperaturas: Optional["ManejaTemperaturas"] = None):
        super().__init__(temperaturas_a_mantener, manejador_temperaturas)
        self._calculadoras_de_estadisticos = dict()

    def manejar_temperatura(self, nueva_temperatura: float):
        super().manejar_temperatura(nueva_temperatura)
        for nombre, calculadora in self._calculadoras_de_estadisticos.items():
            print(f"{nombre}\t: {round(calculadora.aplicar_alg(self._temperaturas), 3)}")

        if self._manejador_temperaturas:
            self._manejador_temperaturas.manejar_temperatura(nueva_temperatura)

    def nueva_calculadora(self, nombre: str, calculadora: CalculadoraEstadistico):
        self._calculadoras_de_estadisticos[nombre] = calculadora


class ComprobadorUmbral(ManejaTemperaturas):
    _umbral: float

    def __init__(self, umbral: float, manejador_temperaturas: Optional["ManejaTemperaturas"] = None):
        super().__init__(1, manejador_temperaturas)
        self._umbral = umbral

    def manejar_temperatura(self, nueva_temperatura: float):
        super().manejar_temperatura(nueva_temperatura)
        print(f"¿Supera la temperatura actual los {self._umbral} grados?", end=" ")
        print("Sí" if self._temperaturas[0] > self._umbral else "No", end=".\n")

        if self._manejador_temperaturas:
            self._manejador_temperaturas.manejar_temperatura(nueva_temperatura)


class ComprobadorDelta(ManejaTemperaturas):
    _delta: float

    def __init__(self, temperaturas_a_mantener: int, delta: float, manejador_temperaturas: Optional["ManejaTemperaturas"] = None):
        self._temperaturas = [0] * temperaturas_a_mantener
        self._indice_actual = 0
        self._temperaturas_a_mantener = temperaturas_a_mantener
        self._is_lista_entera = self._indice_actual == self._temperaturas_a_mantener
        self._delta = delta
        self._manejador_temperaturas = manejador_temperaturas

    def manejar_temperatura(self, nueva_temperatura: float):
        self._temperaturas[self._indice_actual] = nueva_temperatura
        self._indice_actual = (self._indice_actual + 1) % self._temperaturas_a_mantener
        if self._indice_actual == 0 and not self._is_lista_entera:
            self._is_lista_entera = True

        temperatura_a_comparar = self._temperaturas[0] if not self._is_lista_entera else self._temperaturas[self._indice_actual]
        resultado = nueva_temperatura - temperatura_a_comparar >= self._delta
        print(f"En los últimos {(self._temperaturas_a_mantener - 1) * 5} segundos, ¿ha aumentado la temperatura {self._delta} grados?", end=" ")
        print("Sí" if resultado else "No", end=".\n")

        if self._manejador_temperaturas:
            self._manejador_temperaturas.manejar_temperatura(nueva_temperatura)
