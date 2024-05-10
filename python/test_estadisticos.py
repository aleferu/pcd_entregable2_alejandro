import statistics
from entornoiot import (
    CalculadoraMedia,
    CalculadoraModa,
    CalculadoraMax,
    CalculadoraMin,
    CalculadoraQuasiVar,
    CalculadoraMediana
)


################
# Estadísticos #
################


def test_media():
    calculadora = CalculadoraMedia()
    listas_de_prueba = [
        [4, 5, 6],
        list(range(5)),
        [0],
        [1, 2, 3, 4],
        [1.3, 4.5, 8.4]
    ]
    for lista in listas_de_prueba:
        assert calculadora.aplicar_alg(lista) == statistics.mean(lista)


def test_moda():
    calculadora = CalculadoraModa()
    listas_de_prueba = [
        [4, 5, 5, 6],
        [4, 4, 5, 6],
        [4, 5, 6, 6],
        list(range(5)),
        [0],
        [1.3, 4.5, 8.4]
    ]
    for lista in listas_de_prueba:
        #  reversed porque si no hay moda statistics coge el primer valor, mientras que yo el último
        assert calculadora.aplicar_alg(lista) == statistics.mode(reversed(lista))


def test_max():
    calculadora = CalculadoraMax()
    listas_de_prueba = [
        [4, 5, 6],
        list(range(5)),
        [0],
        [1, 2, 3, 4],
        [1.3, 4.5, 8.4]
    ]
    for lista in listas_de_prueba:
        assert calculadora.aplicar_alg(lista) == max(lista)


def test_min():
    calculadora = CalculadoraMin()
    listas_de_prueba = [
        [4, 5, 6],
        list(range(5)),
        [0],
        [1, 2, 3, 4],
        [1.3, 4.5, 8.4]
    ]
    for lista in listas_de_prueba:
        assert calculadora.aplicar_alg(lista) == min(lista)


def test_var():
    calculadora = CalculadoraQuasiVar()
    listas_de_prueba = [
        [4, 5, 6],
        list(range(5)),
        [1, 2, 3, 4],
        [1.3, 4.5, 8.4],
        [5]
    ]
    for lista in listas_de_prueba:
        try:
            assert calculadora.aplicar_alg(lista) == statistics.variance(lista)
        except statistics.StatisticsError:
            assert calculadora.aplicar_alg(lista) == 0


def test_median():
    calculadora = CalculadoraMediana()
    listas_de_prueba = [
        [4, 5, 6],
        list(range(5)),
        [1, 2, 3, 4],
        [1.3, 4.5, 8.4],
        [1.3, 8.4, 4.5],
        [0]
    ]
    for lista in listas_de_prueba:
        assert calculadora.aplicar_alg(lista) == statistics.median(lista)
