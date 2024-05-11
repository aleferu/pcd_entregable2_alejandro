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
        valores_redondeados = list(map(lambda valor: round(valor), valores))
        return reduce(
            lambda moda, candidato: moda if moda[1] > candidato[1] else candidato,
            dict(map(
                lambda valor: (valor, reduce(lambda acc, _: acc + 1, filter(lambda x: x == valor, valores_redondeados), 0)),
                valores_redondeados
            )).items()
        )[0]


class CalculadoraMax(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        return reduce(lambda maximo, candidato: candidato if candidato > maximo else maximo, valores)


class CalculadoraMin(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        return reduce(lambda minimo, candidato: candidato if candidato < minimo else minimo, valores)


class CalculadoraCuasiVar(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        if len(valores) == 1:
            return 0
        media = reduce(lambda acc, x: acc + x, valores) / len(valores)
        return reduce(lambda acc, valor: acc + (valor - media) ** 2, valores, 0) / (len(valores) - 1)


class CalculadoraMediana(CalculadoraEstadistico):
    def aplicar_alg(self, valores: list[float]) -> float:
        half_index = int(len(valores) / 2)
        lista_ordenada = sorted(valores)
        if len(lista_ordenada) % 2 == 1:
            return lista_ordenada[half_index]
        return (lista_ordenada[half_index - 1] + lista_ordenada[half_index]) / 2
