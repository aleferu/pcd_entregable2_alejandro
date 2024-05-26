from abc import ABC, abstractmethod
from functools import reduce


# Se ha forzado mucho el uso de las funciones map, filter y reduce en las implementaciones.
# Incluso en algunos sitios donde se podría haber usado sum, max o min.
# Esto es para demostrar conocimientos, no por eficiencia (seguramente la implementación
# interna sea la más rápida en cada caso, pero habría que hacer pruebas).

# Más específicamente, el cálculo de la moda es mucho más enrevesado de lo que podría ser.


class CalculadoraEstadistico(ABC):
    """
    Clase abstracta que se encarga de ser la cabeza de una jerarquía de clases que
    cumplan con el patrón de diseño de Strategy.

    Todas las clases se encargan de calcular un estadístico a partir de una lista de valores.
    """
    @abstractmethod
    def aplicar_alg(self, valores: list[float]) -> float:
        """
        Método que se encarga de calcular un estadístico.

        Método abstracto, nunca se debe utilizar.

        Parámetros
        ----------
        - valores: lista de números a los cuales hay que calcularles el estadístico

        Lanza
        -----
        - NotImplementedError si se intenta ejecutar.
        """
        raise NotImplementedError("Se ha intentado ejecutar un método abstracto")


class CalculadoraMedia(CalculadoraEstadistico):
    """
    Clase encargada de calcular la media dada una lista de valores.
    """

    def aplicar_alg(self, valores: list[float]) -> float:
        """
        Método encargado de calcular la media de la lista de valores que se pasen.

        Parámetros
        ----------
        - valores: lista de números a los cuales hay que calcularles el estadístico
        """
        return reduce(lambda acc, x: acc + x, valores, 0) / len(valores)


class CalculadoraModa(CalculadoraEstadistico):
    """
    Clase encargada de calcular la moda dada una lista de valores.

    Se calcula la moda de los números redondeados, pues si no fuese así la moda (casi) siempre
    resultaría de un valor que solo se repite una vez.
    """

    def aplicar_alg(self, valores: list[float]) -> float:
        """
        Método encargado de calcular la moda de la lista de valores que se pasen.

        Parámetros
        ----------
        - valores: lista de números a los cuales hay que calcularles el estadístico
        """
        valores_redondeados = list(map(lambda valor: round(valor), valores))
        return reduce(
            lambda moda, candidato: moda if moda[1] > candidato[1] else candidato,
            dict(map(
                lambda valor: (valor, reduce(lambda acc, _: acc + 1, filter(lambda x: x == valor, valores_redondeados), 0)),
                valores_redondeados
            )).items()
        )[0]


class CalculadoraMax(CalculadoraEstadistico):
    """
    Clase encargada de calcular el máximo dada una lista de valores.
    """

    def aplicar_alg(self, valores: list[float]) -> float:
        """
        Método encargado de calcular el máximo de la lista de valores que se pasen.

        Parámetros
        ----------
        - valores: lista de números a los cuales hay que calcularles el estadístico
        """
        return reduce(lambda maximo, candidato: candidato if candidato > maximo else maximo, valores)


class CalculadoraMin(CalculadoraEstadistico):
    """
    Clase encargada de calcular el mínimo dada una lista de valores.
    """

    def aplicar_alg(self, valores: list[float]) -> float:
        """
        Método encargado de calcular el mínimo de la lista de valores que se pasen.

        Parámetros
        ----------
        - valores: lista de números a los cuales hay que calcularles el estadístico
        """
        return reduce(lambda minimo, candidato: candidato if candidato < minimo else minimo, valores)


class CalculadoraCuasiVar(CalculadoraEstadistico):
    """
    Clase encargada de calcular la cuasivarianza dada una lista de valores.
    """

    def aplicar_alg(self, valores: list[float]) -> float:
        """
        Método encargado de calcular la cuasivarianza de la lista de valores que se pasen.

        Parámetros
        ----------
        - valores: lista de números a los cuales hay que calcularles el estadístico
        """
        if len(valores) == 1:
            return 0
        media = reduce(lambda acc, x: acc + x, valores) / len(valores)
        return reduce(lambda acc, valor: acc + (valor - media) ** 2, valores, 0) / (len(valores) - 1)


class CalculadoraMediana(CalculadoraEstadistico):
    """
    Clase encargada de calcular la mediana dada una lista de valores.
    """

    def aplicar_alg(self, valores: list[float]) -> float:
        """
        Método encargado de calcular la mediana de la lista de valores que se pasen.

        Parámetros
        ----------
        - valores: lista de números a los cuales hay que calcularles el estadístico
        """
        half_index = int(len(valores) / 2)
        lista_ordenada = sorted(valores)
        if len(lista_ordenada) % 2 == 1:
            return lista_ordenada[half_index]
        return (lista_ordenada[half_index - 1] + lista_ordenada[half_index]) / 2
