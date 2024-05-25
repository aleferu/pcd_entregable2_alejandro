from abc import ABC
from .estadisticos import CalculadoraEstadistico
from typing import Optional


class ManejaTemperaturas(ABC):
    """
    Clase que se encarga de ser la cabeza de un pratrón de diseño "Chain of Command",
    encargada de recibir temperaturas y hacer algo con ellas.

    Clase abstracta, nunca instanciar.

    Atributos
    ---------
    - _temperaturas: lista de números que representan las temperaturas almacenadas
    - _indice_actual: índice que apunta al índice de la lista que tocaría modificar en el caso de que
    se reciba una nueva temperatura
    - _temperaturas_a_mantener: int que indica el número de temperaturas a mantener, la longitud de '_temperaturas'
    - _is_lista_entera: bool que ayuda al guardado de las temperaturas
    - manejador_temperaturas: instancia de ManejaTemperaturas que sigue en la cadena. Opcional
    """
    _temperaturas: list[float]
    "lista de números que representan las temperaturas almacenadas"

    _indice_actual: int
    "índice que apunta al índice de la lista que tocaría modificar en el caso de que se reciba una nueva temperatura"

    _temperaturas_a_mantener: int
    "int que indica el número de temperaturas a mantener, la longitud de '_temperaturas'"

    _is_lista_entera: bool
    "bool que ayuda al guardado de las temperaturas"

    manejador_temperaturas: Optional["ManejaTemperaturas"]
    "instancia de ManejaTemperatura que sigue en la cadena. Opcional"

    def __init__(self, temperaturas_a_mantener: int, manejador_temperaturas: Optional["ManejaTemperaturas"] = None):
        """
        Crea y devuelve una instancia de ManejaTemperaturas. Sin embargo, esta clase nunca debería inicializarse, solo
        las clases que heredan de esta.

        Parámetros
        ----------
        - temperaturas_a_mantener: int que indica el número de temperaturas a mantener. Número mayor que 0
        - manejador_temperaturas: parámetro opcional que indica el siguiente objeto de la clase ManejaTemperaturas
        """
        self._temperaturas = list()
        self._indice_actual = 0
        self._temperaturas_a_mantener = temperaturas_a_mantener
        self._is_lista_entera = False
        self.manejador_temperaturas = manejador_temperaturas

    def nueva_temperatura(self, nueva_temperatura: float):
        """
        Dada una nueva temperatura, guarda dicha temperatura en la lista, realiza la operación que necesite hacer
        y envía la temperatura al siguiente en la cadena.

        Parámetros
        ----------
        - nueva_temperatura: número que representa la nueva temperatura recibida
        """
        self.manejar_temperatura(nueva_temperatura)
        self.siguiente(nueva_temperatura)

    def manejar_temperatura(self, nueva_temperatura: float):
        """
        Dada una nueva temperatura, guarda dicha temperatura en la lista.

        Parámetros
        ----------
        nueva_temperatura: número que representa la nueva temperatura recibida
        """
        if not self._is_lista_entera:
            self._temperaturas.append(nueva_temperatura)
        else:
            self._temperaturas[self._indice_actual] = nueva_temperatura
        self._indice_actual = (self._indice_actual + 1) % self._temperaturas_a_mantener
        if self._indice_actual == 0 and not self._is_lista_entera:
            self._is_lista_entera = True

    def siguiente(self, temperatura: float):
        """
        Método encargado de enviar una temperatura a la cadena.

        Parámetros
        ----------
        - nueva_temperatura: número que representa temperatura a enviar
        """
        if self.manejador_temperaturas:
            self.manejador_temperaturas.nueva_temperatura(temperatura)


class CalculaEstadisticos(ManejaTemperaturas):
    """
    Clase que se encarga de, cada vez que le llega una temperatura, calcular los estadísticos
    que sean necesarios. Después, si la cadena de comando tiene que seguir, la sigue.

    Atributos
    ---------
    - _temperaturas: lista de números que representan las temperaturas almacenadas
    - _indice_actual: índice que apunta al índice de la lista que tocaría modificar en el caso de que
    se reciba una nueva temperatura
    - _temperaturas_a_mantener: int que indica el número de temperaturas a mantener, la longitud de '_temperaturas'
    - _is_lista_entera: bool que ayuda al guardado de las temperaturas
    - manejador_temperaturas: instancia de ManejaTemperaturas que sigue en la cadena. Opcional
    - _calculadoras_de_estadisticos: diccionario de claves str y valores CalculadoraEstadistico que representa
    los estadísticos a calcular
    """
    _calculadoras_de_estadisticos: dict[str, CalculadoraEstadistico]
    "diccionario de claves str y valores CalculadoraEstadistico que representa los estadísticos a calcular"

    def __init__(self, temperaturas_a_mantener: int, manejador_temperaturas: Optional["ManejaTemperaturas"] = None):
        """
        Crea y devuelve una instancia de CalculaEstadisticos.

        Parámetros
        ----------
        - temperaturas_a_mantener: int que indica el número de temperaturas a mantener. Número mayor que 0
        - manejador_temperaturas: parámetro opcional que indica el siguiente objeto de la clase ManejaTemperaturas
        """
        super().__init__(temperaturas_a_mantener, manejador_temperaturas)
        self._calculadoras_de_estadisticos = dict()

    def manejar_temperatura(self, nueva_temperatura: float):
        """
        Dada una nueva temperatura, guarda dicha temperatura en la lista y calcula los estadísticos. El resultado
        es impreso en pantalla.

        Parámetros
        ----------
        - nueva_temperatura: número que representa la nueva temperatura recibida
        """
        super().manejar_temperatura(nueva_temperatura)
        for nombre, calculadora in self._calculadoras_de_estadisticos.items():
            print(f"{nombre}\t: {round(calculadora.aplicar_alg(self._temperaturas), 3)}")

    def nueva_calculadora(self, nombre: str, calculadora: CalculadoraEstadistico):
        """
        Guarda una nueva calculadora en el diccionario de temperaturas.

        Parámetros
        ----------
        - nombre: str que representa el nombre que se le da al estadístico
        - calculadora: instancia de CalculadoraEstadistico
        """
        self._calculadoras_de_estadisticos[nombre] = calculadora


class ComprobadorUmbral(ManejaTemperaturas):
    """
    Clase que se encarga de, cada vez que le llega una temperatura, comprobar si se ha superado
    cierto umbral. Después, si la cadena de comando tiene que seguir, la sigue.

    Atributos
    ---------
    - _temperaturas: lista de números que representan las temperaturas almacenadas
    - _indice_actual: índice que apunta al índice de la lista que tocaría modificar en el caso de que
    se reciba una nueva temperatura
    - _temperaturas_a_mantener: int que indica el número de temperaturas a mantener, la longitud de '_temperaturas'
    - _is_lista_entera: bool que ayuda al guardado de las temperaturas
    - manejador_temperaturas: instancia de ManejaTemperaturas que sigue en la cadena. Opcional
    - _umbral: número que representa el umbral que hay que vigilar
    """
    _umbral: float
    "número que representa el umbral que hay que vigilar"

    def __init__(self, umbral: float, manejador_temperaturas: Optional["ManejaTemperaturas"] = None):
        """
        Crea y devuelve una instancia de ComprobadorUmbral.

        Parámetros
        ----------
        - umbral: número que representa el umbral que hay que vigilar
        - manejador_temperaturas: parámetro opcional que indica el siguiente objeto de la clase ManejaTemperaturas
        """
        super().__init__(1, manejador_temperaturas)
        self.set_umbral(umbral)

    def manejar_temperatura(self, nueva_temperatura: float):
        """
        Dada una nueva temperatura, guarda dicha temperatura en la lista y realiza la comprobación. El resultado
        es impreso en pantalla.

        Parámetros
        ----------
        - nueva_temperatura: número que representa la nueva temperatura recibida
        """
        super().manejar_temperatura(nueva_temperatura)
        print(f"¿Supera la temperatura actual los {self._umbral} grados?", end=" ")
        print("Sí" if self._temperaturas[0] > self._umbral else "No", end=".\n")

    def set_umbral(self, umbral: float):
        """
        Establece un nuevo umbral.

        Parámetros
        ----------
        - umbral: número que representa el nuevo umbral
        """
        self._umbral = umbral


class ComprobadorDelta(ManejaTemperaturas):
    """
    Clase que se encarga de, cada vez que le llega una temperatura, comprobar si la temperatura ha aumentado
    una cierta cantidad. Después, si la cadena de comando tiene que seguir, la sigue.

    Atributos
    ---------
    - _temperaturas: lista de números que representan las temperaturas almacenadas
    - _indice_actual: índice que apunta al índice de la lista que tocaría modificar en el caso de que
    se reciba una nueva temperatura
    - _temperaturas_a_mantener: int que indica el número de temperaturas a mantener, la longitud de '_temperaturas'
    - _is_lista_entera: bool que ayuda al guardado de las temperaturas
    - manejador_temperaturas: instancia de ManejaTemperaturas que sigue en la cadena. Opcional
    - _delta: número que representa la variación de temperatura a comprobar
    """
    _delta: float
    "número que representa la variación de temperatura a comprobar"

    def __init__(self, temperaturas_a_mantener: int, delta: float, manejador_temperaturas: Optional["ManejaTemperaturas"] = None):
        """
        Crea y devuelve una instancia de ComprobadorDelta.

        Parámetros
        ----------
        - temperaturas_a_mantener: int que indica el número de temperaturas a mantener. Número mayor que 0
        - delta: número que representa la variación de temperatura a comprobar
        - manejador_temperaturas: parámetro opcional que indica el siguiente objeto de la clase ManejaTemperaturas
        """
        self._temperaturas = [0] * temperaturas_a_mantener
        self._indice_actual = 0
        self._temperaturas_a_mantener = temperaturas_a_mantener
        self._is_lista_entera = False
        self.set_delta(delta)
        self.manejador_temperaturas = manejador_temperaturas

    def manejar_temperatura(self, nueva_temperatura: float):
        """
        Dada una nueva temperatura, guarda dicha temperatura en la lista y realiza la comprobación. El resultado
        es impreso en pantalla.

        Parámetros
        ----------
        - nueva_temperatura: número que representa la nueva temperatura recibida
        """
        self._temperaturas[self._indice_actual] = nueva_temperatura
        self._indice_actual = (self._indice_actual + 1) % self._temperaturas_a_mantener
        if self._indice_actual == 0 and not self._is_lista_entera:
            self._is_lista_entera = True

        temperatura_a_comparar = self._temperaturas[0] if not self._is_lista_entera else self._temperaturas[self._indice_actual]
        resultado = nueva_temperatura - temperatura_a_comparar >= self._delta
        print(f"En los últimos {(self._temperaturas_a_mantener - 1) * 5} segundos, ¿ha aumentado la temperatura {self._delta} grados?", end=" ")
        print("Sí" if resultado else "No", end=".\n")

    def set_delta(self, delta: float):
        """
        Establece un nuevo delta.

        Parámetros
        ----------
        - delta: número que representa el nuevo delta
        """
        self._delta = delta
