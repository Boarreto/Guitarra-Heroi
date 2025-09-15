import var
import pygame   # Biblioteca
import random
import time

# ----------------------
# region    1. HUD

class Contador:
    def __init__(self):
        self.valor = 0

class ContadorErros:
    def __init__(self):
        self.valor = 0

# endregion

# ----------------------
# region    2. Hit

class Hit:
    def __init__(self, imagem, x, yInicial, teclaHit, velocidade):
        self.imagem = imagem
        self.x = x
        self.y = yInicial
        self.teclaHit = teclaHit
        self.ativa = True
        self.pontuada = False 
        self.velocidade = velocidade
        
    
    def atualizar(self):
        if self.y < 600:  # Verifica se a nota ainda esta na tela
            self.y += self.velocidade
    
    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))
    
    def verificarHit(self, event, contador):
        if event.type == pygame.KEYDOWN and event.key == self.teclaHit:
            if self.ativa and var.ativacaoInicial < self.y < var.ativacaoFinal:
                contador.valor += 1
                self.pontuada = True     # marca como pontuada
                self.ativa = False       # desativa para não contar de novo

    def removerHit(self):
        return self.pontuada or self.y >= 600
    
    def errou(self):
        return self.y >= 600 and not self.pontuada


# endregion

# ----------------------
# region    3. Funcoes

    # Processa evento
def processarEventos(notas, contador):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        for nota in notas:
            nota.verificarHit(event, contador)
    return True

    # Desenha a tela
def desenhar():
    screen.blit(imgFundo, (0, 0))
    for nota in notas:
        nota.desenhar(screen)
    screen.blit(imgGuitarRed, (var.guitarRed_x, var.guitarRed_y))
    screen.blit(imgGuitarBlue, (var.guitarBlue_x, var.guitarBlue_y))
    screen.blit(imgBarraAtivacao, (var.barraAtv_x, var.barraAtv_y))
    texto_pontos = font.render(f"Pontos: {contador.valor}", True, (255, 255, 255))
    texto_erros = font.render(f"Erros: {contadorErros.valor}", True, (255, 0, 0))
    texto_tempo = font.render(f"Tempo: {duracao_fase - tempo_passado}s", True, (255, 255, 255))
    screen.blit(texto_pontos, (20, 20))
    screen.blit(texto_erros, (20, 50))
    screen.blit(texto_tempo, (20, 80))

    # Mostra menu inicial
def mostrar_menu(screen, font):
    menu_running = True
    dificuldade = None
    fall_speed = None
    intervalo_spawn = None

    while menu_running:
        screen.fill((0, 0, 0))  # Fundo preto

        # Textos
        titulo = font.render("Guitarra Heroi", True, (255, 255, 255))
        instrucao = font.render("Escolha a dificuldade:", True, (255, 255, 255))
        facil = font.render("[1] Fácil", True, (0, 255, 0))
        medio = font.render("[2] Médio", True, (255, 255, 0))
        dificil = font.render("[3] Difícil", True, (255, 0, 0))

        # Desenha textos na tela
        screen.blit(titulo, (250, 100))
        screen.blit(instrucao, (220, 200))
        screen.blit(facil, (300, 300))
        screen.blit(medio, (300, 350))
        screen.blit(dificil, (300, 400))

        pygame.display.flip()

        # Captura eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    dificuldade = "facil"
                    fall_speed = 3
                    intervalo_spawn = 0.8
                    menu_running = False
                elif event.key == pygame.K_2:
                    dificuldade = "medio"
                    fall_speed = 5
                    intervalo_spawn = 0.5
                    menu_running = False
                elif event.key == pygame.K_3:
                    dificuldade = "dificil"
                    fall_speed = 7
                    intervalo_spawn = 0.3
                    menu_running = False

    return dificuldade, fall_speed, intervalo_spawn


# endregion

#           4. Iniciando Jogo
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# ----------------------
# region    5. Carregando imagens

imgFundo = (pygame.image.load("assets/fundo.png").convert_alpha())

imgGuitarRed = (pygame.image.load("assets/guitar-red.png").convert_alpha())
imgGuitarRed = pygame.transform.scale(imgGuitarRed, (128, 128))

imgGuitarBlue = (pygame.image.load("assets/guitar-blue.png").convert_alpha())
imgGuitarBlue = pygame.transform.scale(imgGuitarBlue, (128, 128))

imgHitVerde = (pygame.image.load("assets/hitVerde.png").convert_alpha())
imgHitVerde = pygame.transform.scale(imgHitVerde, (64, 64))

imgHitVermelho = (pygame.image.load("assets/HitVermelho.png").convert_alpha())
imgHitVermelho = pygame.transform.scale(imgHitVermelho, (64, 64))

imgHitAmarelo = (pygame.image.load("assets/HitAmarelo.png").convert_alpha())
imgHitAmarelo = pygame.transform.scale(imgHitAmarelo, (64, 64))

imgHitAzul = (pygame.image.load("assets/HitAzul.png").convert_alpha())
imgHitAzul = pygame.transform.scale(imgHitAzul, (64, 64))

imgBarraAtivacao = (pygame.image.load("assets/barra-ativacao.png").convert_alpha())
imgBarraAtivacao = pygame.transform.scale(imgBarraAtivacao, (600, 40))

# endregion

# ----------------------
# region    6. Configuracoes

contador = Contador()
contadorErros = ContadorErros()
notas = []
font = pygame.font.SysFont(None, 48)

#   Lanes disponiveis [ATALHOS]
#       VERDE ->        A
#       VERMELHO ->     S
#       AMARELO ->      D
#       AZUL ->         F
lanes = [
    {"x": var.hitVerde_x, "tecla": pygame.K_a, "imagem": imgHitVerde}, 
    {"x": var.hitVermelho_x, "tecla": pygame.K_s, "imagem": imgHitVermelho},
    {"x": var.hitAmarelo_x, "tecla": pygame.K_d, "imagem": imgHitAmarelo},
    {"x": var.hitAzul_x, "tecla": pygame.K_f, "imagem": imgHitAzul},
]

# Temporizador da fase
duracao_fase = var.tempoMusica1  # segundos
inicio_fase = time.time()

# Controle de tempo para spawn
ultimo_spawn = time.time()
intervalo_spawn = random.uniform(0.25, 0.5)  # segundos

# endregion

# ----------------------
# region    7. Menu inicial

dificuldade, var.fallSpeed, intervalo_spawn = mostrar_menu(screen, font) # Chama menu

ultimo_spawn = time.time() # Segue loop

# endregion

# ----------------------
# region    8. Loop principal

running = True
while running:
    
    # Iniciar tempo
    agora = time.time()
    tempo_passado = int(agora - inicio_fase)
    # Encerrar fase apos tempo
    if tempo_passado >= duracao_fase:
        running = False

    # 7. Processa eventos
    processarEventos(notas, contador)
    

# A cada segundo, decidir se cria uma nova nota
    if agora - ultimo_spawn > intervalo_spawn:
        lane = random.choice(lanes) # Selecionar uma lane aleatoria

        # Criar nova nota nessa lane
        notas.append(Hit(lane["imagem"], lane["x"], 0, lane["tecla"], var.fallSpeed))

        # Atualizar o tempo de spawn e intervalo
        ultimo_spawn = agora
        intervalo_spawn = random.uniform(0.25, 0.5)

    # 8. Criar notas
    for nota in notas: 
        nota.atualizar()
        nota.desenhar(screen) # Desenha as notas

    # Remove hit se acertar (se dentro de notas) e remove se sair da tela
    novas_notas = []
    for nota in notas:
        if nota.removerHit():
            if nota.errou():
                contadorErros.valor += 1
        else:
            novas_notas.append(nota)
    notas = novas_notas

    # Desenhar HUD
    desenhar()

    pygame.display.flip() 
    clock.tick(60) # Limitado para 60FPS

# endregion

pygame.quit()
