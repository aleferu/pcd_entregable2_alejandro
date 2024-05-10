from abc import ABC
from .estadisticos import CalculadoraEstadistico
from typing import Optional


class ManejaTemperaturas(ABC):
    temperaturas: list[float]
    indice_actual: int
    temperaturas_a_mantener: int
    is_lista_entera: bool
    manejador_temperaturas: Optional["ManejaTemperaturas"]

    def __init__(self, temperaturas_a_mantener: int, manejador_temperaturas: Optional["ManejaTemperaturas"] = None):
        self.temperaturas = list()
        self.indice_actual = 0
        self.temperaturas_a_mantener = temperaturas_a_mantener
        self.is_lista_entera = self.indice_actual == self.temperaturas_a_mantener
        self.manejador_temperaturas = manejador_temperaturas

    def manejar_temperatura(self, nueva_temperatura: float):
        if not self.is_lista_entera:
            self.temperaturas.append(nueva_temperatura)
        else:
            self.temperaturas[self.indice_actual] = nueva_temperatura
        self.indice_actual = (self.indice_actual + 1) % self.temperaturas_a_mantener
        if self.indice_actual == 0 and not self.is_lista_entera:
            self.is_lista_entera = True


class CalculaEstadisticos(ManejaTemperaturas):
    calculadoras_de_estadisticos: dict[str, CalculadoraEstadistico]

    def __init__(self, temperaturas_a_mantener: int):
        super().__init__(temperaturas_a_mantener)
        self.calculadoras_de_estadisticos = dict()

    def manejar_temperatura(self, nueva_temperatura: float):
        super().manejar_temperatura(nueva_temperatura)
        for nombre, calculadora in self.calculadoras_de_estadisticos.items():
            print(f"{nombre}\t: {round(calculadora.aplicar_alg(self.temperaturas), 3)}")

        if self.manejador_temperaturas:
            self.manejador_temperaturas.manejar_temperatura(nueva_temperatura)

    def nueva_calculadora(self, nombre: str, calculadora: CalculadoraEstadistico):
        self.calculadoras_de_estadisticos[nombre] = calculadora


class ComprobadorUmbral(ManejaTemperaturas):
    umbral: float

    def __init__(self, temperaturas_a_mantener: int, umbral: float):
        super().__init__(temperaturas_a_mantener)
        self.umbral = umbral

    def manejar_temperatura(self, nueva_temperatura: float):
        super().manejar_temperatura(nueva_temperatura)
        print(f"¿Supera la temperatura los {self.umbral} grados?", end=" ")
        print("Sí" if self.temperaturas[0] > self.umbral else "No", end=".\n")

        if self.manejador_temperaturas:
            self.manejador_temperaturas.manejar_temperatura(nueva_temperatura)


class ComprobadorDelta(ManejaTemperaturas):
    delta: float

    def __init__(self, temperaturas_a_mantener: int, delta: float):
        self.temperaturas = [0] * temperaturas_a_mantener
        self.indice_actual = 0
        self.temperaturas_a_mantener = temperaturas_a_mantener
        self.is_lista_entera = self.indice_actual == self.temperaturas_a_mantener
        self.delta = delta

    def manejar_temperatura(self, nueva_temperatura: float):
        super().manejar_temperatura(nueva_temperatura)
        temperatura_a_comparar = self.temperaturas[0] if not self.is_lista_entera else self.temperaturas[self.indice_actual]
        resultado = abs(nueva_temperatura - temperatura_a_comparar) > self.delta
        print(f"En los últimos {self.temperaturas_a_mantener * 5} segundos, ha aumentado la temperatura {self.delta} grados?", end=" ")
        print("Sí" if resultado else "No", end=".\n")

        if self.manejador_temperaturas:
            self.manejador_temperaturas.manejar_temperatura(nueva_temperatura)
