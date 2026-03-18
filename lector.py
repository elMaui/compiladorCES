# Archivo: lector.py
# Responsable: Persona 1

class LectorFuente:
    """
    Se encarga de leer el código fuente carácter por carácter,
    manteniendo el control exacto de la línea y columna actual.
    """
    def __init__(self, codigo_fuente: str):
        self.codigo = codigo_fuente
        self.posicion = 0
        self.linea = 1
        self.columna = 1

    def hay_mas_caracteres(self) -> bool:
        """Devuelve True si aún no llegamos al final del archivo."""
        return self.posicion < len(self.codigo)

    def mirar_actual(self) -> str:
        """
        Devuelve el carácter en la posición actual SIN avanzar.
        Si ya no hay caracteres, devuelve un carácter nulo.
        """
        if self.hay_mas_caracteres():
            return self.codigo[self.posicion]
        return '\0'  # Simboliza el Fin de Archivo (EOF)

    def mirar_siguiente(self) -> str:
        """
        Devuelve el carácter que le sigue al actual SIN avanzar.
        Muy útil para detectar operadores dobles como '==' o '<='.
        """
        if self.posicion + 1 < len(self.codigo):
            return self.codigo[self.posicion + 1]
        return '\0'

    def avanzar(self) -> str:
        """
        Devuelve el carácter actual y avanza los punteros de posición,
        línea y columna.
        """
        if not self.hay_mas_caracteres():
            return '\0'
        
        caracter = self.codigo[self.posicion]
        self.posicion += 1
        
        # Si detectamos un salto de línea, ajustamos las coordenadas
        if caracter == '\n':
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
            
        return caracter

    def saltar_espacios_y_comentarios(self):
        """
        Avanza automáticamente si encuentra espacios en blanco, tabulaciones,
        saltos de línea o comentarios (// y /* */).
        """
        while self.hay_mas_caracteres():
            actual = self.mirar_actual()
            siguiente = self.mirar_siguiente()

            # 1. Ignorar espacios en blanco, tabs y saltos de línea
            if actual in [' ', '\t', '\n', '\r']:
                self.avanzar()
                
            # 2. Ignorar comentarios de una línea: //
            elif actual == '/' and siguiente == '/':
                # Avanzamos hasta encontrar un salto de línea o el fin de archivo
                while self.hay_mas_caracteres() and self.mirar_actual() != '\n':
                    self.avanzar()
                    
            # 3. Ignorar comentarios multilinea: /* ... */
            elif actual == '/' and siguiente == '*':
                self.avanzar() # Consumimos '/'
                self.avanzar() # Consumimos '*'
                
                # Avanzamos hasta encontrar '*/'
                while self.hay_mas_caracteres():
                    if self.mirar_actual() == '*' and self.mirar_siguiente() == '/':
                        self.avanzar() # Consumimos '*'
                        self.avanzar() # Consumimos '/'
                        break
                    self.avanzar()
            
            # Si no es espacio ni comentario, detenemos el salto
            else:
                break