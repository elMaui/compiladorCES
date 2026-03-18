# Archivo: main.py
# Responsable: Persona 4

import sys
from lector import LectorFuente
from lexer import AnalizadorLexico
from tokens import TipoToken

def principal():
    # 1. Obtener la ruta del archivo de entrada
    # Permite ejecutar: python main.py mi_codigo.c_esp
    if len(sys.argv) > 1:
        ruta_archivo = sys.argv[1]
    else:
        print("Uso: python main.py <archivo_fuente>")
        print("Aviso: No se proporcionó archivo por terminal. Intentando leer 'prueba.c_esp' por defecto.\n")
        ruta_archivo = "prueba.c_esp"

    # 2. Leer el contenido del código fuente
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            codigo_fuente = archivo.read()
    except FileNotFoundError:
        print(f"Error fatal: No se encontró el archivo '{ruta_archivo}'.")
        return

    # 3. Inicializar los componentes creados por el equipo
    lector = LectorFuente(codigo_fuente)
    lexer = AnalizadorLexico(lector)

    tokens_procesados = []
    errores_lexicos = 0

    print(f"--- Iniciando Análisis Léxico de '{ruta_archivo}' ---\n")

    # 4. Ciclo principal del Analizador (Motor)
    while True:
        token = lexer.siguiente_token()
        
        # Manejo de Errores (Panic Mode básico)
        if token.tipo == TipoToken.ERROR:
            # Imprimimos el error claramente pero NO detenemos el programa
            print(f"¡ERROR LÉXICO! Carácter inesperado '{token.lexema}' en Línea: {token.linea}, Columna: {token.columna}")
            errores_lexicos += 1
            continue # Saltamos este token inválido y seguimos analizando el resto del código

        # Agregamos el token válido a nuestra lista y lo imprimimos en consola
        tokens_procesados.append(token)
        print(token) # Esto llama automáticamente al método __str__ de la Persona 2

        # Condición de salida: Si llegamos al End Of File
        if token.tipo == TipoToken.EOF:
            break

    # 5. Generar el archivo de salida con los resultados
    archivo_salida = "salida_tokens.txt"
    with open(archivo_salida, 'w', encoding='utf-8') as f_salida:
        for t in tokens_procesados:
            f_salida.write(str(t) + '\n')

    # 6. Resumen de ejecución
    print("\n--- Análisis Terminado ---")
    print(f"Total de tokens generados: {len(tokens_procesados)}")
    print(f"Total de errores léxicos: {errores_lexicos}")
    print(f"El reporte completo se ha guardado en '{archivo_salida}'")

if __name__ == "__main__":
    principal()