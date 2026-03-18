# Archivo: tokens.py
# Responsable: Persona 2

from enum import Enum

class TipoToken(Enum):
    # --- Palabras Reservadas ---
    ENTERO = "ENTERO"
    FLOTANTE = "FLOTANTE"
    VACIO = "VACIO"
    SI = "SI"
    SINO = "SINO"
    MIENTRAS = "MIENTRAS"
    REGRESA = "REGRESA"
    IMPRIMIR = "IMPRIMIR"

    # --- Identificadores y Literales ---
    IDENTIFICADOR = "IDENTIFICADOR"
    NUM_ENTERO = "NUM_ENTERO"
    NUM_FLOTANTE = "NUM_FLOTANTE"
    CADENA = "CADENA"

    # --- Operadores Matemáticos y Lógicos ---
    ASIGNACION = "ASIGNACION"         # =
    SUMA = "SUMA"                     # +
    RESTA = "RESTA"                   # -
    MULTIPLICACION = "MULTIPLICACION" # *
    DIVISION = "DIVISION"             # /
    IGUAL_QUE = "IGUAL_QUE"           # ==
    DIFERENTE_DE = "DIFERENTE_DE"     # !=
    MENOR_QUE = "MENOR_QUE"           # <
    MAYOR_QUE = "MAYOR_QUE"           # >
    MENOR_O_IGUAL = "MENOR_O_IGUAL"   # <=
    MAYOR_O_IGUAL = "MAYOR_O_IGUAL"   # >=
    AND = "AND"                       # &&
    OR = "OR"                         # ||

    # --- Símbolos de Puntuación y Agrupación ---
    PAREN_IZQ = "PAREN_IZQ"           # (
    PAREN_DER = "PAREN_DER"           # )
    LLAVE_IZQ = "LLAVE_IZQ"           # {
    LLAVE_DER = "LLAVE_DER"           # }
    PUNTO_COMA = "PUNTO_COMA"         # ;
    COMA = "COMA"                     # ,

    # --- Tokens Especiales ---
    EOF = "EOF"                       # Fin de archivo (End Of File)
    ERROR = "ERROR"                   # Para caracteres no válidos

# Diccionario para búsqueda ultrarrápida de palabras reservadas.
# La Persona 3 (Motor) usará esto para saber si un texto es variable o palabra clave.
PALABRAS_RESERVADAS = {
    "entero": TipoToken.ENTERO,
    "flotante": TipoToken.FLOTANTE,
    "vacio": TipoToken.VACIO,
    "si": TipoToken.SI,
    "sino": TipoToken.SINO,
    "mientras": TipoToken.MIENTRAS,
    "regresa": TipoToken.REGRESA,
    "imprimir": TipoToken.IMPRIMIR
}

class Token:
    """
    Clase que representa un componente léxico individual.
    """
    def __init__(self, tipo: TipoToken, lexema: str, linea: int, columna: int):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __str__(self):
        """
        Define cómo se imprime el token. 
        Formato de salida esperado: <TIPO, "lexema", Linea: X, Col: Y>
        """
        return f'<{self.tipo.name}, "{self.lexema}", Linea: {self.linea}, Col: {self.columna}>'

    def __repr__(self):
        # Permite que las listas de tokens se impriman bien en consola para depurar
        return self.__str__()