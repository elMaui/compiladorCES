# Archivo: lexer.py
# Responsable: Persona 3

from tokens import TipoToken, Token, PALABRAS_RESERVADAS
from lector import LectorFuente

class AnalizadorLexico:
    """
    Motor principal del analizador léxico. Agrupa los caracteres
    proporcionados por el LectorFuente para construir Tokens.
    """
    def __init__(self, lector: LectorFuente):
        self.lector = lector

    def siguiente_token(self) -> Token:
        """
        Evalúa los caracteres y devuelve el siguiente Token válido (o un ERROR).
        """
        # 1. Limpiar el camino de espacios y comentarios
        self.lector.saltar_espacios_y_comentarios()

        # 2. Verificar si llegamos al final del archivo
        if not self.lector.hay_mas_caracteres():
            return Token(TipoToken.EOF, "", self.lector.linea, self.lector.columna)

        # Guardamos la posición inicial del token para el reporte
        linea_inicio = self.lector.linea
        columna_inicio = self.lector.columna
        
        # Leemos el primer carácter
        c = self.lector.avanzar()

        # --- REGLA 1: Identificadores y Palabras Reservadas ---
        if c.isalpha() or c == '_':
            lexema = c
            # Seguimos leyendo mientras sean letras, números o guiones bajos
            while self.lector.mirar_actual().isalnum() or self.lector.mirar_actual() == '_':
                lexema += self.lector.avanzar()
            
            # Verificamos si el lexema formado es una palabra reservada
            tipo = PALABRAS_RESERVADAS.get(lexema, TipoToken.IDENTIFICADOR)
            return Token(tipo, lexema, linea_inicio, columna_inicio)

        # --- REGLA 2: Números (Enteros y Flotantes) ---
        if c.isdigit():
            lexema = c
            es_flotante = False
            
            while self.lector.mirar_actual().isdigit():
                lexema += self.lector.avanzar()
            
            # Verificamos si tiene parte decimal
            if self.lector.mirar_actual() == '.':
                es_flotante = True
                lexema += self.lector.avanzar() # Consumimos el punto
                # Leemos los decimales
                while self.lector.mirar_actual().isdigit():
                    lexema += self.lector.avanzar()
            
            tipo = TipoToken.NUM_FLOTANTE if es_flotante else TipoToken.NUM_ENTERO
            return Token(tipo, lexema, linea_inicio, columna_inicio)

        # --- REGLA 3: Cadenas de Texto ---
        if c == '"':
            lexema = c
            while self.lector.hay_mas_caracteres() and self.lector.mirar_actual() != '"':
                lexema += self.lector.avanzar()
            
            if self.lector.mirar_actual() == '"':
                lexema += self.lector.avanzar() # Consumimos la comilla de cierre
            return Token(TipoToken.CADENA, lexema, linea_inicio, columna_inicio)

        # --- REGLA 4: Operadores Dobles (==, !=, <=, >=, &&, ||) ---
        siguiente = self.lector.mirar_actual()
        
        if c == '=' and siguiente == '=':
            self.lector.avanzar()
            return Token(TipoToken.IGUAL_QUE, "==", linea_inicio, columna_inicio)
        if c == '!' and siguiente == '=':
            self.lector.avanzar()
            return Token(TipoToken.DIFERENTE_DE, "!=", linea_inicio, columna_inicio)
        if c == '<' and siguiente == '=':
            self.lector.avanzar()
            return Token(TipoToken.MENOR_O_IGUAL, "<=", linea_inicio, columna_inicio)
        if c == '>' and siguiente == '=':
            self.lector.avanzar()
            return Token(TipoToken.MAYOR_O_IGUAL, ">=", linea_inicio, columna_inicio)
        if c == '&' and siguiente == '&':
            self.lector.avanzar()
            return Token(TipoToken.AND, "&&", linea_inicio, columna_inicio)
        if c == '|' and siguiente == '|':
            self.lector.avanzar()
            return Token(TipoToken.OR, "||", linea_inicio, columna_inicio)

        # --- REGLA 5: Operadores Simples y Símbolos de Puntuación ---
        simbolos_simples = {
            '=': TipoToken.ASIGNACION,
            '+': TipoToken.SUMA,
            '-': TipoToken.RESTA,
            '*': TipoToken.MULTIPLICACION,
            '/': TipoToken.DIVISION,
            '<': TipoToken.MENOR_QUE,
            '>': TipoToken.MAYOR_QUE,
            '(': TipoToken.PAREN_IZQ,
            ')': TipoToken.PAREN_DER,
            '{': TipoToken.LLAVE_IZQ,
            '}': TipoToken.LLAVE_DER,
            ';': TipoToken.PUNTO_COMA,
            ',': TipoToken.COMA
        }

        if c in simbolos_simples:
            return Token(simbolos_simples[c], c, linea_inicio, columna_inicio)

        # --- REGLA 6: Caracteres no reconocidos (Error Léxico) ---
        return Token(TipoToken.ERROR, c, linea_inicio, columna_inicio)