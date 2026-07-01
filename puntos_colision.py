"""
Puntos en movimiento con colisiones.

Interfaz 2D donde varios puntos se mueven de forma aleatoria dentro de la
ventana. Cuando dos puntos se encuentran (colisionan), ambos desaparecen.

Requisitos:
    pip install pygame

Uso:
    python puntos_colision.py

Controles:
    - ESC o cerrar la ventana: salir.
    - R: reiniciar con un nuevo conjunto de puntos.
    - ESPACIO: pausar / reanudar.
"""

import math
import random
import sys

import pygame

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
ANCHO, ALTO = 800, 600      # Tamaño de la ventana en píxeles.
NUM_PUNTOS = 40             # Cantidad inicial de puntos.
RADIO = 6                   # Radio de cada punto.
VELOCIDAD_MAX = 3.0         # Velocidad máxima (px por frame) en cada eje.
FPS = 60                    # Fotogramas por segundo.
COLOR_FONDO = (18, 18, 24)
COLOR_TEXTO = (230, 230, 230)


class Punto:
    """Un punto que se mueve en línea recta y rebota en los bordes."""

    def __init__(self):
        self.x = random.uniform(RADIO, ANCHO - RADIO)
        self.y = random.uniform(RADIO, ALTO - RADIO)
        # Velocidad aleatoria distinta de cero en cada eje.
        self.vx = random.uniform(-VELOCIDAD_MAX, VELOCIDAD_MAX) or 1.0
        self.vy = random.uniform(-VELOCIDAD_MAX, VELOCIDAD_MAX) or 1.0
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
        )

    def mover(self):
        """Avanza un paso y rebota contra los bordes de la ventana."""
        self.x += self.vx
        self.y += self.vy

        # Rebote horizontal.
        if self.x - RADIO <= 0:
            self.x = RADIO
            self.vx = abs(self.vx)
        elif self.x + RADIO >= ANCHO:
            self.x = ANCHO - RADIO
            self.vx = -abs(self.vx)

        # Rebote vertical.
        if self.y - RADIO <= 0:
            self.y = RADIO
            self.vy = abs(self.vy)
        elif self.y + RADIO >= ALTO:
            self.y = ALTO - RADIO
            self.vy = -abs(self.vy)

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), RADIO)


def hay_colision(a, b):
    """Devuelve True si los puntos a y b se tocan (distancia < 2*RADIO)."""
    dx = a.x - b.x
    dy = a.y - b.y
    return math.hypot(dx, dy) < RADIO * 2


def detectar_colisiones(puntos):
    """Devuelve el conjunto de índices de puntos que colisionan entre sí."""
    eliminados = set()
    total = len(puntos)
    for i in range(total):
        for j in range(i + 1, total):
            if i in eliminados and j in eliminados:
                continue
            if hay_colision(puntos[i], puntos[j]):
                eliminados.add(i)
                eliminados.add(j)
    return eliminados


def crear_puntos():
    return [Punto() for _ in range(NUM_PUNTOS)]


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Puntos en movimiento con colisiones")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 18)

    puntos = crear_puntos()
    pausado = False

    while True:
        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_r:
                    puntos = crear_puntos()
                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado

        # --- Actualización ---
        if not pausado:
            for punto in puntos:
                punto.mover()

            eliminados = detectar_colisiones(puntos)
            if eliminados:
                puntos = [p for k, p in enumerate(puntos) if k not in eliminados]

        # --- Dibujado ---
        pantalla.fill(COLOR_FONDO)
        for punto in puntos:
            punto.dibujar(pantalla)

        info = f"Puntos: {len(puntos)}   [R] reiniciar  [ESPACIO] pausa  [ESC] salir"
        if pausado:
            info += "   (PAUSA)"
        pantalla.blit(fuente.render(info, True, COLOR_TEXTO), (10, 10))

        pygame.display.flip()
        reloj.tick(FPS)


if __name__ == "__main__":
    main()
