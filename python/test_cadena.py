from entornoiot import (
    CalculaEstadisticos,
    ComprobadorUmbral,
    ComprobadorDelta,
    CalculadoraMedia,
    CalculadoraCuasiVar
)


######################
# ManejaTemperaturas #
######################


# CalculaEstadisticos


def test_calcula_estadisticos_inicializado_correctamente():
    objeto0 = CalculaEstadisticos(2)
    assert len(objeto0._temperaturas) == 0
    assert objeto0._indice_actual == 0
    assert objeto0._temperaturas_a_mantener == 2
    assert not objeto0._is_lista_entera
    assert not objeto0.manejador_temperaturas
    assert len(objeto0._calculadoras_de_estadisticos) == 0

    objeto1 = CalculaEstadisticos(4, objeto0)
    assert objeto1.manejador_temperaturas is objeto0


# Al parecer capsys se usa para capturar el output de un test
# Fuente: https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html
def test_calcula_estadisticos_correctamente(capsys):
    calcula_estadisticos = CalculaEstadisticos(2)
    calcula_estadisticos.nueva_calculadora("Media", CalculadoraMedia())
    calcula_estadisticos.nueva_calculadora("Varianza", CalculadoraCuasiVar())
    assert len(calcula_estadisticos._calculadoras_de_estadisticos) == 2
    assert isinstance(calcula_estadisticos._calculadoras_de_estadisticos["Media"], CalculadoraMedia)
    assert isinstance(calcula_estadisticos._calculadoras_de_estadisticos["Varianza"], CalculadoraCuasiVar)

    calcula_estadisticos.manejar_temperatura(1)
    out, _ = capsys.readouterr()
    assert out == "Media\t: 1.0\nVarianza\t: 0\n"
    assert calcula_estadisticos._temperaturas == [1]

    calcula_estadisticos.manejar_temperatura(2)
    out, _ = capsys.readouterr()
    assert out == "Media\t: 1.5\nVarianza\t: 0.5\n"
    assert calcula_estadisticos._is_lista_entera
    assert calcula_estadisticos._temperaturas == [1, 2]

    calcula_estadisticos.manejar_temperatura(3)
    out, _ = capsys.readouterr()
    assert out == "Media\t: 2.5\nVarianza\t: 0.5\n"
    assert calcula_estadisticos._temperaturas == [3, 2]


def test_calcula_estadisticos_cadena(capsys):
    calcula_estadisticos0 = CalculaEstadisticos(2)
    calcula_estadisticos0.nueva_calculadora("Varianza", CalculadoraCuasiVar())

    calcula_estadisticos1 = CalculaEstadisticos(3, calcula_estadisticos0)
    calcula_estadisticos1.nueva_calculadora("Media", CalculadoraMedia())

    calcula_estadisticos1.manejar_temperatura(1)
    out, _ = capsys.readouterr()
    assert out == "Media\t: 1.0\nVarianza\t: 0\n"

    calcula_estadisticos1.manejar_temperatura(2)
    out, _ = capsys.readouterr()
    assert out == "Media\t: 1.5\nVarianza\t: 0.5\n"

    calcula_estadisticos1.manejar_temperatura(3)
    out, _ = capsys.readouterr()
    assert out == "Media\t: 2.0\nVarianza\t: 0.5\n"


# ComprobadorUmbral


def test_comprobador_umbral_inicializado_correctamente():
    objeto0 = ComprobadorUmbral(5)
    assert len(objeto0._temperaturas) == 0
    assert objeto0._indice_actual == 0
    assert objeto0._temperaturas_a_mantener == 1
    assert not objeto0._is_lista_entera
    assert not objeto0.manejador_temperaturas
    assert objeto0._umbral == 5

    objeto1 = ComprobadorUmbral(4, objeto0)
    assert objeto1.manejador_temperaturas is objeto0


def test_comprobador_umbral(capsys):
    umbral = 5
    comprobador_umbral = ComprobadorUmbral(umbral)

    comprobador_umbral.manejar_temperatura(1)
    out, _ = capsys.readouterr()
    assert out == f"¿Supera la temperatura actual los {umbral} grados? No.\n"
    assert comprobador_umbral._is_lista_entera

    comprobador_umbral.manejar_temperatura(5)
    out, _ = capsys.readouterr()
    assert out == f"¿Supera la temperatura actual los {umbral} grados? No.\n"

    comprobador_umbral.manejar_temperatura(6)
    out, _ = capsys.readouterr()
    assert out == f"¿Supera la temperatura actual los {umbral} grados? Sí.\n"


def test_comprobador_umbral_cadena(capsys):
    umbral0 = 2
    comprobador_umbral0 = ComprobadorUmbral(umbral0)
    umbral1 = 3
    comprobador_umbral1 = ComprobadorUmbral(umbral1, comprobador_umbral0)

    comprobador_umbral1.manejar_temperatura(1.5)
    out, _ = capsys.readouterr()
    assert out == f"¿Supera la temperatura actual los {umbral1} grados? No.\n" +\
        f"¿Supera la temperatura actual los {umbral0} grados? No.\n"

    comprobador_umbral1.manejar_temperatura(2.5)
    out, _ = capsys.readouterr()
    assert out == f"¿Supera la temperatura actual los {umbral1} grados? No.\n" +\
        f"¿Supera la temperatura actual los {umbral0} grados? Sí.\n"

    comprobador_umbral1.manejar_temperatura(3.5)
    out, _ = capsys.readouterr()
    assert out == f"¿Supera la temperatura actual los {umbral1} grados? Sí.\n" +\
        f"¿Supera la temperatura actual los {umbral0} grados? Sí.\n"


# ComprobadorDelta


def test_comprobador_delta_inicializado_correctamente():
    objeto0 = ComprobadorDelta(3, 5)
    assert len(objeto0._temperaturas) == 3
    assert objeto0._indice_actual == 0
    assert objeto0._temperaturas_a_mantener == 3
    assert not objeto0._is_lista_entera
    assert not objeto0.manejador_temperaturas
    assert objeto0._delta == 5

    objeto1 = ComprobadorDelta(4, 6, objeto0)
    assert objeto1.manejador_temperaturas is objeto0


def test_comprobador_delta(capsys):
    temperaturas_a_mantener = 2
    delta = 5
    comprobador_delta = ComprobadorDelta(temperaturas_a_mantener, delta)

    comprobador_delta.manejar_temperatura(1)
    out, _ = capsys.readouterr()
    assert out == f"En los últimos {(temperaturas_a_mantener - 1) * 5} segundos, ¿ha aumentado la temperatura {delta} grados? No.\n"
    assert comprobador_delta._temperaturas == [1, 0]

    comprobador_delta.manejar_temperatura(6)
    out, _ = capsys.readouterr()
    assert out == f"En los últimos {(temperaturas_a_mantener - 1) * 5} segundos, ¿ha aumentado la temperatura {delta} grados? Sí.\n"
    assert comprobador_delta._is_lista_entera
    assert comprobador_delta._temperaturas == [1, 6]

    comprobador_delta.manejar_temperatura(5)
    out, _ = capsys.readouterr()
    assert out == f"En los últimos {(temperaturas_a_mantener - 1) * 5} segundos, ¿ha aumentado la temperatura {delta} grados? No.\n"
    assert comprobador_delta._temperaturas == [5, 6]

    comprobador_delta.manejar_temperatura(15)
    out, _ = capsys.readouterr()
    assert out == f"En los últimos {(temperaturas_a_mantener - 1) * 5} segundos, ¿ha aumentado la temperatura {delta} grados? Sí.\n"
    assert comprobador_delta._temperaturas == [5, 15]


def test_comprobador_delta_cadena(capsys):
    temperaturas_a_mantener0 = 2
    delta0 = 2
    comprobador_delta0 = ComprobadorDelta(temperaturas_a_mantener0, delta0)
    temperaturas_a_mantener1 = 3
    delta1 = 3
    comprobador_delta1 = ComprobadorDelta(temperaturas_a_mantener1, delta1, comprobador_delta0)

    comprobador_delta1.manejar_temperatura(0.5)
    out, _ = capsys.readouterr()
    assert out == f"En los últimos {(temperaturas_a_mantener1 - 1) * 5} segundos, ¿ha aumentado la temperatura {delta1} grados? No.\n" +\
        f"En los últimos {(temperaturas_a_mantener0 - 1) * 5} segundos, ¿ha aumentado la temperatura {delta0} grados? No.\n"

    comprobador_delta1.manejar_temperatura(2.5)
    out, _ = capsys.readouterr()
    assert out == f"En los últimos {(temperaturas_a_mantener1 - 1) * 5} segundos, ¿ha aumentado la temperatura {delta1} grados? No.\n" +\
        f"En los últimos {(temperaturas_a_mantener0 - 1) * 5} segundos, ¿ha aumentado la temperatura {delta0} grados? Sí.\n"

    comprobador_delta1.manejar_temperatura(15)
    out, _ = capsys.readouterr()
    assert out == f"En los últimos {(temperaturas_a_mantener1 - 1) * 5} segundos, ¿ha aumentado la temperatura {delta1} grados? Sí.\n" +\
        f"En los últimos {(temperaturas_a_mantener0 - 1) * 5} segundos, ¿ha aumentado la temperatura {delta0} grados? Sí.\n"
