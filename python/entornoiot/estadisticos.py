#!/usr/bin/env python3


from abc import ABC, abstractmethod
from functools import reduce


class CalculadoraEstadistico(ABC):
    @abstractmethod
    def aplicar_alg(self, valores: list[float]) -> float:
        pass


class CalculadoraMedia(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        return reduce(lambda acc, x: acc + x, valores, 0) / len(valores)


class CalculadoraModa(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        return reduce(
            lambda moda, candidato: moda if moda[1] > candidato[1] else candidato,
            dict(map(
                lambda valor: (valor, reduce(lambda acc, _: acc + 1, filter(lambda x: x == valor, valores), 0)),
                valores
            )).items()
        )[0]


class CalculadoraMax(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        return max(valores)


class CalculadoraMin(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        return min(valores)


class CalculadoraQuasiVar(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        media = reduce(lambda acc, x: acc + x, valores) / len(valores)
        return reduce(lambda acc, valor: acc + (valor - media) ** 2, valores, 0) / (len(valores) - 1)


class CalculadoraMediana(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        half_index = int(len(valores) / 2)
        print(half_index)
        if len(valores) % 2 == 1:
            return valores[half_index]
        return (valores[half_index - 1] + valores[half_index]) / 2
