import random


class Jugador:
    def __init__(self, simbolo, nombre):
        """Inicializa un jugador con su símbolo y nombre."""
        self.simbolo = simbolo
        self.nombre = nombre

    def realizar_jugada(self, tablero):
        """Método base para realizar una jugada. Lo implementan las subclases."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")


class Computadora(Jugador):
    def __init__(self, simbolo, nivel_dificultad="fácil", nombre="Computadora"):
        super().__init__(simbolo, nombre)
        self.nivel_dificultad = nivel_dificultad  # Podemos ponerla en dificil

    def realizar_jugada(self, tablero):
        """La computadora elige una jugada según su nivel de dificultad."""
        posicion = self.elegir_jugada(tablero)
        print(f"{self.nombre} juega en {posicion + 1}")
        tablero[posicion] = self.simbolo

    def elegir_jugada(self, tablero):
        """La computadora elige una jugada según su nivel de dificultad."""
        if self.nivel_dificultad == "fácil":
            return self.jugada_aleatoria(tablero)
        elif self.nivel_dificultad == "media":
            return self.jugada_media(tablero)
        elif self.nivel_dificultad == "difícil":
            return self.jugada_dificil(tablero)

    def movimientos_disponibles(self, tablero):
        """Devuelve las posiciones vacías en el tablero."""
        return [i for i, casilla in enumerate(tablero) if casilla == " "]

    def jugada_aleatoria(self, tablero):
        """Elige una jugada aleatoria."""
        return random.choice(self.movimientos_disponibles(tablero))

    def jugada_media(self, tablero):
        """La computadora bloquea jugadas ganadoras del humano o elige aleatoriamente."""
        # Bloquear jugadas ganadoras del jugador
        for posicion in self.movimientos_disponibles(tablero):
            tablero_copia = tablero[:]
            tablero_copia[posicion] = "C"  # Supón que juega la computadora
            if self.verificar_ganador(tablero_copia):
                return posicion

        # Bloquear jugadas ganadoras del humano
        for posicion in self.movimientos_disponibles(tablero):
            tablero_copia = tablero[:]
            tablero_copia[posicion] = "H"  # Supón que juega el humano
            if self.verificar_ganador(tablero_copia):
                return posicion

        # Si no hay jugadas ganadoras, elige aleatoriamente
        return self.jugada_aleatoria(tablero)

    def jugada_dificil(self, tablero):
        """La computadora elige la mejor jugada usando una versión simple de Minimax."""
        # La estrategia minimax busca la jugada que maximiza las oportunidades de ganar
        mejor_jugada = None
        mejor_valor = -float("inf")

        for posicion in self.movimientos_disponibles(tablero):
            tablero_copia = tablero[:]
            tablero_copia[posicion] = "C"
            valor = self.minimax(tablero_copia, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_jugada = posicion

        return mejor_jugada

    def minimax(self, tablero, es_maximizando):
        """Algoritmo Minimax para calcular el valor de una jugada."""
        ganador = self.verificar_ganador(tablero)
        if ganador == "C":
            return 1  # La computadora gana
        elif ganador == "H":
            return -1  # El humano gana
        elif not self.movimientos_disponibles(tablero):
            return 0  # Empate

        if es_maximizando:
            mejor_valor = -float("inf")
            for posicion in self.movimientos_disponibles(tablero):
                tablero_copia = tablero[:]
                tablero_copia[posicion] = "C"
                valor = self.minimax(tablero_copia, False)
                mejor_valor = max(mejor_valor, valor)
            return mejor_valor
        else:
            mejor_valor = float("inf")
            for posicion in self.movimientos_disponibles(tablero):
                tablero_copia = tablero[:]
                tablero_copia[posicion] = "H"
                valor = self.minimax(tablero_copia, True)
                mejor_valor = min(mejor_valor, valor)
            return mejor_valor

    def verificar_ganador(self, tablero):
        """Verifica si hay un ganador en el tablero."""
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Filas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columnas
            (0, 4, 8), (2, 4, 6)  # Diagonales
        ]
        for a, b, c in combinaciones:
            if tablero[a] == tablero[b] == tablero[c] and tablero[a] != " ":
                return tablero[a]
        return None


class Humano(Jugador):
    def __init__(self, simbolo, nombre="Humano"):
        super().__init__(simbolo, nombre)

    def realizar_jugada(self, tablero):
        """El jugador humano elige una posición en el tablero."""
        while True:
            try:
                posicion = int(input(f"{self.nombre}, elige una posición (1-9): ")) - 1
                if 0 <= posicion < 9 and tablero[posicion] == " ":
                    tablero[posicion] = self.simbolo
                    break
                else:
                    print("Posición inválida. Intenta de nuevo.")
            except ValueError:
                print("Por favor, ingresa un número válido.")


class Juego:
    def __init__(self):
        """Inicializa el juego."""
        self.tablero = [" "] * 9
        self.jugadores = []
        self.turno = None
        self.ganador = None
        self.estadisticas = {"humano": 0, "computadora": 0, "empates": 0}  # Estadísticas

    def mostrar_estadisticas(self):
        """Muestra las estadísticas de la partida."""
        print(
            f"Estadísticas:\nHumano: {self.estadisticas['humano']} | Computadora: {self.estadisticas['computadora']} | Empates: {self.estadisticas['empates']}")

    def seleccionar_dificultad(self):
        """Permite al jugador elegir el nivel de dificultad de la computadora."""
        print("Selecciona el nivel de dificultad para la computadora:")
        print("1 - Fácil")
        print("2 - Media")
        print("3 - Difícil")
        while True:
            try:
                opcion = int(input("Elige una opción (1, 2, 3): "))
                if opcion == 1:
                    return "fácil"
                elif opcion == 2:
                    return "media"
                elif opcion == 3:
                    return "difícil"
                else:
                    print("Opción inválida, intenta de nuevo.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

    def mostrar_tablero(self):
        """Muestra el tablero de juego con una presentación mejorada."""
        # Definimos colores (se pueden omitir si no quieres usar colores)
        VACIO = "\033[90m"  # Gris para espacios vacíos
        HUMANO = "\033[92m"  # Verde para el humano
        COMPUTADORA = "\033[94m"  # Azul para la computadora
        RESET = "\033[0m"  # Resetear color

        # Establecemos un formato para el tablero
        print("\n" + " ╔═══╦═══╦═══╗ ")
        for i in range(0, 9, 3):
            print(f" ║ {self.colorear(self.tablero[i], VACIO, HUMANO, COMPUTADORA)} ║ "
                  f"{self.colorear(self.tablero[i + 1], VACIO, HUMANO, COMPUTADORA)} ║ "
                  f"{self.colorear(self.tablero[i + 2], VACIO, HUMANO, COMPUTADORA)} ║ ")

            if i < 6:
                print(" ╠═══╬═══╬═══╣ ")

        print(" ╚═══╩═══╩═══╝ \n")

    def mostrar_tablero(self):
        """Muestra el tablero de juego con una presentación mejorada."""
        # Definimos colores (se pueden omitir si no quieres usar colores)
        VACIO = "\033[90m"  # Gris para espacios vacíos
        HUMANO = "\033[92m"  # Verde para el humano
        COMPUTADORA = "\033[94m"  # Azul para la computadora
        RESET = "\033[0m"  # Resetear color

        # Establecemos un formato para el tablero
        print("\n" + " ╔═══╦═══╦═══╗ ")
        for i in range(0, 9, 3):
            print(f" ║ {self.colorear(self.tablero[i], VACIO, HUMANO, COMPUTADORA, RESET)} ║ "
                  f"{self.colorear(self.tablero[i + 1], VACIO, HUMANO, COMPUTADORA, RESET)} ║ "
                  f"{self.colorear(self.tablero[i + 2], VACIO, HUMANO, COMPUTADORA, RESET)} ║ ")

            if i < 6:
                print(" ╠═══╬═══╬═══╣ ")

        print(" ╚═══╩═══╩═══╝ \n")


    def colorear(self, simbolo, VACIO, HUMANO, COMPUTADORA, RESET):
        """Devuelve el símbolo con el color correspondiente sin agregar espacios extras."""
        if simbolo == " ":
            return f"{VACIO}{simbolo}{RESET}"  # Espacio vacío
        elif simbolo == "H":
            return f"{HUMANO}{simbolo}{RESET}"  # Casilla ocupada por el humano
        elif simbolo == "C":
            return f"{COMPUTADORA}{simbolo}{RESET}"  # Casilla ocupada por la computadora
        return simbolo

    def verificar_ganador(self):
        """Verifica si hay un ganador en el tablero."""
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Filas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columnas
            (0, 4, 8), (2, 4, 6)  # Diagonales
        ]
        for a, b, c in combinaciones:
            if self.tablero[a] == self.tablero[b] == self.tablero[c] and self.tablero[a] != " ":
                return self.tablero[a]
        return None

    def movimientos_disponibles(self):
        """Devuelve una lista con las posiciones vacías en el tablero."""
        return [i for i in range(9) if self.tablero[i] == " "]

    def determinar_turno_inicial(self, dado_humano, dado_computadora):
        """Determina quién empieza el juego según el resultado de los dados."""
        return self.jugadores[0] if dado_humano >= dado_computadora else self.jugadores[1]

    def lanzar_dado(self):
        """Lanza un dado de 6 caras."""
        return random.randint(1, 6)

    def jugar(self):
        """Inicia y maneja el flujo del juego."""
        print("¡Bienvenido al Juego del Gato!")

        nivel_dificultad = self.seleccionar_dificultad()

        while True:
            self.tablero = [" "] * 9
            # Cambiar dificultad
            self.jugadores = [Humano("H"), Computadora("C", nivel_dificultad=nivel_dificultad)]
            dado_humano = self.lanzar_dado()
            dado_computadora = self.lanzar_dado()
            print(f"Lanzamiento del dado: Humano {dado_humano}, Computadora {dado_computadora}")

            self.turno = self.determinar_turno_inicial(dado_humano, dado_computadora)
            print(f"Empieza: {self.turno.nombre}")

            while self.movimientos_disponibles():
                self.mostrar_tablero()
                self.turno.realizar_jugada(self.tablero)
                self.turno = self.jugadores[0] if self.turno == self.jugadores[1] else self.jugadores[1]

                self.ganador = self.verificar_ganador()
                if self.ganador:
                    self.mostrar_tablero()
                    if self.ganador == "H":
                        print("¡El humano gana!")
                        self.estadisticas["humano"] += 1
                    elif self.ganador == "C":
                        print("¡La computadora gana!")
                        self.estadisticas["computadora"] += 1
                    break

            if not self.movimientos_disponibles():
                self.mostrar_tablero()
                print("¡Es un empate!")
                self.estadisticas["empates"] += 1

            self.mostrar_estadisticas()

            jugar_de_nuevo = input("¿Deseas jugar nuevamente? (0 = Sí, 1 = No): ")
            if jugar_de_nuevo == "1":
                break


def main():
    """Función principal que maneja la ejecución del juego."""
    # Cambir nivel de dificultad en codigo al instanciar la Computadora
    juego = Juego()
    juego.jugar()


# Ejecutar el juego solo si este archivo es ejecutado directamente
if __name__ == "__main__":
    main()
