import pygame
import random

pygame.init()

ANCHO, ALTO = 800, 600
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 120, 255)
VERDE = (0, 255, 0)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Lanzamiento de Dados")
fuente = pygame.font.Font(None, 36)
fuente_titulo = pygame.font.Font(None, 72)

controles = {
    "Lanzar Dados": pygame.K_SPACE,
    "Reiniciar": pygame.K_r,
    "Pausa": pygame.K_ESCAPE,
}


def dibujar_texto(texto, x, y, color=BLANCO, fuente=fuente):
    superficie = fuente.render(texto, True, color)
    rectangulo = superficie.get_rect()
    rectangulo.center = (x, y)
    pantalla.blit(superficie, rectangulo)


def dibujar_dado(valor, x, y):
    lado = 100
    pygame.draw.rect(
        pantalla, BLANCO, (x - lado // 2, y - lado // 2, lado, lado), border_radius=15
    )
    pygame.draw.rect(
        pantalla, NEGRO, (x - lado // 2, y - lado // 2, lado, lado), 5, border_radius=15
    )
    puntos = {
        1: [(0, 0)],
        2: [(-25, -25), (25, 25)],
        3: [(-25, -25), (0, 0), (25, 25)],
        4: [(-25, -25), (25, -25), (-25, 25), (25, 25)],
        5: [(-25, -25), (25, -25), (0, 0), (-25, 25), (25, 25)],
        6: [(-25, -25), (25, -25), (-25, 0), (25, 0), (-25, 25), (25, 25)],
    }
    for dx, dy in puntos[valor]:
        pygame.draw.circle(pantalla, ROJO, (x + dx, y + dy), 10)


def personalizar_controles():
    fuente = pygame.font.Font(None, 36)
    fuente_Titulo = pygame.font.Font(None, 46)
    fuente_instrucciones = pygame.font.Font(None, 26)
    global controles
    seleccion = 0
    opciones = list(controles.keys())
    esperando_tecla = False
    gris_claro = (200, 200, 200)
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente_Titulo.render("Personalizar Controles", True, BLANCO)
        pantalla.blit(
            texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 6)
        )
        for i, opcion in enumerate(opciones):
            color = AZUL if i == seleccion else BLANCO
            texto = f"{opcion.capitalize()}: {pygame.key.name(controles[opcion])}"
            if esperando_tecla and i == seleccion:
                texto = f"{opcion.capitalize()}: Presiona una tecla..."
            texto_renderizado = fuente.render(texto, True, color)
            pantalla.blit(
                texto_renderizado,
                (ANCHO // 2 - texto_renderizado.get_width() // 2, ALTO // 3 + i * 50),
            )
        texto_instruccion = fuente_instrucciones.render(
            "Presiona ENTER para personalizar", True, gris_claro
        )
        pantalla.blit(
            texto_instruccion,
            (ANCHO // 2 - texto_instruccion.get_width() // 2, ALTO - 100),
        )
        texto_volver = fuente_instrucciones.render(
            "Presiona ESC para volver", True, gris_claro
        )
        pantalla.blit(
            texto_volver, (ANCHO // 2 - texto_volver.get_width() // 2, ALTO - 60)
        )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if not esperando_tecla:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return
                    elif evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones)
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones)
                    elif evento.key == pygame.K_RETURN:
                        esperando_tecla = True
            else:
                if evento.type == pygame.KEYDOWN:
                    controles[opciones[seleccion]] = evento.key
                    esperando_tecla = False
        pygame.display.flip()


def menu_principal():
    seleccion = 0
    opciones = ["Jugar", "Personalizar Controles", "Salir"]
    while True:
        pantalla.fill(NEGRO)
        dibujar_texto(
            "Lanzamiento de dados", ANCHO // 2, ALTO // 4, BLANCO, fuente_titulo
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            dibujar_texto(opcion, ANCHO // 2, ALTO // 2 + i * 50, color)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return True
                    elif seleccion == 1:
                        personalizar_controles()
                    elif seleccion == 2:
                        pygame.quit()
                        return False
        pygame.display.flip()


def menu_pausa():
    fuente = pygame.font.Font(None, 74)
    fuente_pequeña = pygame.font.Font(None, 36)
    seleccion = 0
    opciones = ["Reanudar", "Reiniciar", "Salir al menú principal"]
    while True:
        pantalla.fill(NEGRO)
        texto_pausa = fuente.render("Pausa", True, BLANCO)
        pantalla.blit(
            texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return "reanudar"
                    elif seleccion == 1:
                        return "reiniciar"
                    elif seleccion == 2:
                        return "menu_principal"
        pygame.display.flip()


def lanzar_dados():
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    return dado1, dado2, dado1 + dado2


def main():
    while True:
        if not menu_principal():
            break
        dado1, dado2, suma = lanzar_dados()
        lanzamientos = 0
        historial = []
        juego_en_curso = True
        while juego_en_curso:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == controles["Lanzar Dados"]:
                        dado1, dado2, suma = lanzar_dados()
                        lanzamientos += 1
                        historial.append(suma)
                    elif evento.key == controles["Reiniciar"]:
                        dado1, dado2, suma = lanzar_dados()
                        lanzamientos = 0
                        historial.clear()
                    elif evento.key == controles["Pausa"]:
                        opcion = menu_pausa()
                        if opcion == "reiniciar":
                            dado1, dado2, suma = lanzar_dados()
                            lanzamientos = 0
                            historial.clear()
                        elif opcion == "menu_principal":
                            juego_en_curso = False
                            break
            pantalla.fill(NEGRO)
            if lanzamientos > 0:
                dibujar_dado(dado1, ANCHO // 3, ALTO // 2)
                dibujar_dado(dado2, 2 * ANCHO // 3, ALTO // 2)
            else:
                dibujar_dado(1, ANCHO // 3, ALTO // 2)
                dibujar_dado(1, 2 * ANCHO // 3, ALTO // 2)
            dibujar_texto(f"Suma: {suma}", ANCHO // 2, ALTO // 2 + 150)
            dibujar_texto(f"Lanzamientos: {lanzamientos}", ANCHO // 2, ALTO - 50)
            dibujar_texto("Presiona ESPACIO para lanzar", ANCHO // 2, 50)
            dibujar_texto("Presiona 'R' para reiniciar", ANCHO // 2, 100)
            if historial:
                historial_texto = "Historial: " + ", ".join(map(str, historial))
                dibujar_texto(historial_texto, ANCHO // 2, ALTO // 2 + 200, AZUL)
            pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
