'''

'''

import random

def mostrar_instrucciones():
    """Muestra las instrucciones del juego al inicio."""
    print("=== BIENVENIDO A BATALLA NAVAL ===")
    print("Instrucciones:")
    print("1. El juego se desarrolla en un tablero de 10x10.")
    print("2. Los valores válidos para filas y columnas son del 0 al 10.")
    print("3. Cada jugador colocará 3 barcos:")
    print("   - Submarino (tamaño 2).")
    print("   - Acorazado (tamaño 3).")
    print("   - Buque de guerra (tamaño 4).")
    print("4. Los barcos pueden colocarse horizontal o verticalmente.")
    print("5. No se pueden solapar los barcos ni salir de los límites del tablero.")
    print("6. El juego terminará tras 5 rondas o cuando todos los barcos de un jugador sean hundidos.")
    print("=" * 50)

def crear_tablero():
    """Crea un tablero vacío de 10x10."""
    return [["~"] * 11 for _ in range(11)]

def mostrar_tablero(tablero, ocultar_barcos=False):
    """Muestra el tablero en consola. Opción para ocultar barcos del enemigo."""
    print("  " + " ".join(map(str, range(11))))
    for idx, fila in enumerate(tablero):
        if ocultar_barcos:
            print(f"{idx} " + " ".join("~" if celda == "B" else celda for celda in fila))
        else:
            print(f"{idx} " + " ".join(fila))

def validar_colocacion(tablero, fila, columna, direccion, tamaño):
    """
    Valida si un barco se puede colocar en una posición específica.
    - dirección: "H" para horizontal, "V" para vertical.
    """
    if direccion == "H":
        if columna + tamaño > 11:
            return False  # El barco se sale del tablero
        for i in range(tamaño):
            if tablero[fila][columna + i] == "B":
                return False  # Choca con otro barco
    elif direccion == "V":
        if fila + tamaño > 11:
            return False  # El barco se sale del tablero
        for i in range(tamaño):
            if tablero[fila + i][columna] == "B":
                return False  # Choca con otro barco
    return True

def colocar_barco(tablero, nombre, tamaño):
    """Permite al jugador colocar un barco en el tablero."""
    print(f"\nColoca tu {nombre} (tamaño {tamaño}).")
    while True:
        try:
            coordenadas = input(f"Introduce las coordenadas iniciales (fila,columna) del {nombre}: ").strip()
            fila, columna = map(int, coordenadas.split(","))
            direccion = input("¿En qué dirección quieres colocarlo? (H para horizontal, V para vertical): ").strip().upper()
            if direccion not in ["H", "V"]:
                print("Dirección inválida. Debe ser 'H' o 'V'. Inténtalo de nuevo.")
                continue
            if validar_colocacion(tablero, fila, columna, direccion, tamaño):
                if direccion == "H":
                    for i in range(tamaño):
                        tablero[fila][columna + i] = "B"
                elif direccion == "V":
                    for i in range(tamaño):
                        tablero[fila + i][columna] = "B"
                break
            else:
                print("No se puede colocar el barco aquí. Revisa las coordenadas e inténtalo de nuevo.")
        except ValueError:
            print("Entrada inválida. Asegúrate de usar el formato correcto (fila,columna).")
        except IndexError:
            print("Coordenadas fuera del rango. Inténtalo de nuevo.")

def realizar_ataque(tablero, fila, columna):
    """
    Realiza un ataque a las coordenadas dadas.
    Retorna True si se golpea un barco, False si no.
    """
    if tablero[fila][columna] == "B":
        tablero[fila][columna] = "X"
        print("¡Impacto!")
        return True
    elif tablero[fila][columna] == "~":
        tablero[fila][columna] = "O"
        print("Fallaste. Agua.")
        return False
    else:
        print("Ya atacaste esta posición. Intenta otra coordenada.")
        return False

def verificar_barcos_restantes(tablero):
    """Verifica si quedan barcos en el tablero."""
    for fila in tablero:
        if "B" in fila:
            return True
    return False

def jugar():
    """Flujo principal del juego."""
    mostrar_instrucciones()

    # Crear tableros
    tablero_jugador = crear_tablero()
    tablero_oponente = crear_tablero()

    # Colocar barcos del jugador
    print("\nJugador, coloca tus barcos.")
    mostrar_tablero(tablero_jugador)
    colocar_barco(tablero_jugador, "Submarino", 2)
    colocar_barco(tablero_jugador, "Acorazado", 3)
    colocar_barco(tablero_jugador, "Buque de guerra", 4)
    print("\nTus barcos han sido colocados.")
    mostrar_tablero(tablero_jugador)

    # Colocar barcos del oponente (aleatorio)
    for tamaño in [2, 3, 4]:
        while True:
            fila, columna = random.randint(0, 10), random.randint(0, 10)
            direccion = random.choice(["H", "V"])
            if validar_colocacion(tablero_oponente, fila, columna, direccion, tamaño):
                if direccion == "H":
                    for i in range(tamaño):
                        tablero_oponente[fila][columna + i] = "B"
                elif direccion == "V":
                    for i in range(tamaño):
                        tablero_oponente[fila + i][columna] = "B"
                break

    # Inicio del juego
    rondas = 5
    for ronda in range(1, rondas + 1):
        print(f"\n=== RONDA {ronda} ===")
        print("\nTu tablero:")
        mostrar_tablero(tablero_jugador)
        print("\nTablero del oponente:")
        mostrar_tablero(tablero_oponente, ocultar_barcos=True)

        # Ataque del jugador
        while True:
            try:
                ataque = input("Introduce las coordenadas de tu ataque (fila,columna): ").strip()
                fila, columna = map(int, ataque.split(","))
                if 0 <= fila <= 10 and 0 <= columna <= 10:
                    if realizar_ataque(tablero_oponente, fila, columna):
                        if not verificar_barcos_restantes(tablero_oponente):
                            print("¡Ganaste! Hundiste todos los barcos del oponente.")
                            return
                    break
                else:
                    print("Coordenadas fuera del rango. Inténtalo de nuevo.")
            except ValueError:
                print("Entrada inválida. Asegúrate de usar el formato correcto (fila,columna).")

        # Ataque del oponente (aleatorio)
        while True:
            fila, columna = random.randint(0, 10), random.randint(0, 10)
            if tablero_jugador[fila][columna] not in ["X", "O"]:
                print(f"El oponente ataca las coordenadas ({fila},{columna}).")
                realizar_ataque(tablero_jugador, fila, columna)
                if not verificar_barcos_restantes(tablero_jugador):
                    print("¡Perdiste! Todos tus barcos han sido hundidos.")
                    return
                break

    print("\n=== FIN DEL JUEGO ===")
    print("¡Gracias por jugar Batalla Naval!")

# Iniciar el juego
jugar()
